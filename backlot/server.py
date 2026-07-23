"""Backlot 服务器 —— FastAPI 应用：看板状态 API、SSE 变更推送、媒体服务。

watcher 通过 watchfiles 监听 ``projects/`` 目录；一旦发生变更，它会递增
对应项目的版本号并唤醒 SSE 订阅者，由订阅者通知浏览器重新拉取状态。
服务器绝不会写入项目目录。
"""

from __future__ import annotations

import asyncio
import os
import json
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backlot.state import PROJECTS_DIR, REPO_ROOT, list_projects, load_board_state, summarize_project

UI_DIR = Path(__file__).resolve().parent / "ui"
THUMB_CACHE_DIR = REPO_ROOT / ".backlot" / "thumbs"
THUMB_WIDTHS = (320, 640, 960)

# Paths inside a project whose changes are pure noise for the board.
_IGNORE_PARTS = {"node_modules", ".git", "__pycache__", ".cache"}

SSE_HEARTBEAT_SECONDS = 15


def _ui_html(name: str, assets: tuple[str, ...]) -> HTMLResponse:
    html = (UI_DIR / name).read_text(encoding="utf-8")
    for asset in assets:
        path = UI_DIR / asset
        if path.is_file():
            version = str(int(path.stat().st_mtime))
            html = html.replace(f"/ui/{asset}", f"/ui/{asset}?v={version}")
    return HTMLResponse(html)


class ChangeHub:
    """Fan-out of project-change notifications to SSE subscribers.

    Subscriptions are filtered: a board subscribed to one project only ever
    receives that project's ids, so unrelated-project bursts can't flood its
    queue and starve out the one notification it actually needs.
    """

    def __init__(self) -> None:
        self._subscribers: dict[asyncio.Queue, Optional[str]] = {}

    def subscribe(self, project_id: Optional[str] = None) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=64)
        self._subscribers[q] = project_id
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._subscribers.pop(q, None)

    def publish(self, project_id: str) -> None:
        for q, only in list(self._subscribers.items()):
            if only is not None and only != project_id:
                continue
            try:
                q.put_nowait(project_id)
            except asyncio.QueueFull:
                # Queue holds only THIS subscriber's relevant ids, so a full
                # queue already guarantees a pending wake-up → safe to drop.
                pass


hub = ChangeHub()

# Library summaries are expensive to derive (full state parse per project);
# cache per project and invalidate from the watcher.
_summary_cache: dict[str, dict] = {}


def _invalidate_summary(project_id: str) -> None:
    _summary_cache.pop(project_id, None)


def _cached_summaries() -> list[dict]:
    if not PROJECTS_DIR.is_dir():
        return []
    summaries = []
    for entry in sorted(PROJECTS_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith(("_", ".")):
            continue
        cached = _summary_cache.get(entry.name)
        if cached is None:
            try:
                cached = summarize_project(entry)
            except Exception:
                cached = {
                    "project_id": entry.name, "title": entry.name,
                    "pipeline_type": "unknown", "has_pipeline_state": False,
                    "poster": None, "live": False, "last_activity": 0,
                    "active_stage": None, "awaiting_human": False,
                    "stage_states": [], "completed_count": 0,
                    "render_count": 0, "scene_count": 0, "error": "unreadable",
                }
            _summary_cache[entry.name] = cached
        summaries.append(cached)
    summaries.sort(key=lambda s: (not s["live"], -(s["last_activity"] or 0)))
    return summaries


# Watch-loop hot path: pure string comparison, no per-path filesystem calls
# (change batches can be thousands of paths during a render).
import os as _os

_PROJECTS_ROOT_STR = _os.path.normcase(str(PROJECTS_DIR.resolve()))


def _project_of_change(path_str: str) -> Optional[str]:
    """Map a changed filesystem path to a project id (None = irrelevant)."""
    norm = _os.path.normcase(_os.path.normpath(path_str))
    if not norm.startswith(_PROJECTS_ROOT_STR):
        return None
    rel = norm[len(_PROJECTS_ROOT_STR):].lstrip("\\/")
    if not rel:
        return None
    parts = rel.replace("\\", "/").split("/")
    if _IGNORE_PARTS.intersection(parts):
        return None
    return parts[0]


async def _watch_projects() -> None:
    """Background task: watch projects/ and publish debounced changes."""
    try:
        from watchfiles import awatch
    except ImportError:
        return  # watcher unavailable → board still works via manual refresh
    if not PROJECTS_DIR.is_dir():
        return
    async for changes in awatch(PROJECTS_DIR, recursive=True, step=400):
        touched: set[str] = set()
        for _change, path_str in changes:
            pid = _project_of_change(path_str)
            if pid:
                touched.add(pid)
        for pid in touched:
            _invalidate_summary(pid)
            hub.publish(pid)


class CreateProjectRequest(BaseModel):
    title: str
    pipeline_type: str = "cinematic"


class GenerateRequest(BaseModel):
    prompt: str
    mode: str = "image"  # "image" 或 "video"
    image_path: Optional[str] = None  # 图生视频/图生图时的输入图


# ===== 生成任务异步执行支持 =====
# 全局任务存储：task_id -> {status, stage, progress, message, result, error, project_id, mode}
_gen_tasks: dict[str, dict] = {}


def _set_task_stage(task_id: str, stage: str, progress: int, message: str = "") -> None:
    """更新任务阶段（线程安全：GIL 保护下的字典写入）。"""
    t = _gen_tasks.get(task_id)
    if not t:
        return
    t["stage"] = stage
    t["progress"] = progress
    if message:
        t["message"] = message


def _run_gen_task(task_id: str, project_id: str, prompt: str, mode: str, image_path: str | None) -> None:
    """在后台线程中执行实际的生成逻辑。整个函数是同步阻塞的，但运行在线程池中，不会阻塞事件循环。"""
    import os, time, hashlib
    import requests as http_requests

    # 标记任务为运行中
    t0 = _gen_tasks.get(task_id)
    if t0:
        t0["status"] = "running"

    project_dir = _safe_project_dir(project_id)
    api_key = os.environ.get("AGNES_API_KEY", "")
    base_url = os.environ.get("AGNES_API_BASE_URL", "https://apihub.agnes-ai.com/v1")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        if mode == "image":
            # ----- 图片生成 -----
            _set_task_stage(task_id, "submitting", 5, "正在提交图片生成请求...")
            payload = {
                "model": "agnes-image-2.1-flash",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
            }
            if image_path:
                img_full = (project_dir / image_path).resolve()
                try:
                    img_full.relative_to(project_dir.resolve())
                except ValueError:
                    raise RuntimeError("路径越出项目目录")
                import base64
                with open(img_full, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode()
                payload["image"] = f"data:image/png;base64,{img_b64}"

            _set_task_stage(task_id, "calling_api", 15, "Agnes API 生成中...")
            data = None
            for _attempt in range(5):
                try:
                    resp = http_requests.post(f"{base_url}/images/generations", headers=headers, json=payload, timeout=90)
                    if resp.status_code in (429, 502, 503):
                        _set_task_stage(task_id, "calling_api", 15 + _attempt * 5, f"Agnes 繁忙，重试中（第{_attempt+1}次）...")
                        time.sleep(10)
                        continue
                    resp.raise_for_status()
                    data = resp.json()
                    break
                except Exception as e:
                    if _attempt < 4:
                        _set_task_stage(task_id, "calling_api", 15 + _attempt * 5, f"请求异常，重试中（第{_attempt+1}次）: {e}")
                        time.sleep(10)
                    else:
                        raise RuntimeError(f"Agnes API 调用失败（已重试 5 次）: {e}")
            if data is None:
                raise RuntimeError("Agnes API 调用失败：未获取到响应")

            _set_task_stage(task_id, "downloading", 80, "下载图片...")
            img_url = data.get("data", [{}])[0].get("url", "")
            if not img_url:
                img_b64 = data.get("data", [{}])[0].get("b64_json", "")
                if img_b64:
                    img_url = f"data:image/png;base64,{img_b64}"
            if not img_url:
                raise RuntimeError("Agnes API 未返回图片")

            fname = f"{hashlib.md5(prompt.encode()).hexdigest()[:10]}_{int(time.time())}.png"
            save_path = project_dir / "assets" / "images" / fname
            (project_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)

            if img_url.startswith("data:"):
                import base64 as b64mod
                b64_data = img_url.split(",", 1)[1]
                with open(save_path, "wb") as f:
                    f.write(b64mod.b64decode(b64_data))
            else:
                img_resp = http_requests.get(img_url, timeout=60)
                img_resp.raise_for_status()
                with open(save_path, "wb") as f:
                    f.write(img_resp.content)

            _invalidate_summary(project_id)
            hub.publish(project_id)
            _set_task_stage(task_id, "done", 100, "图片生成完成")
            _gen_tasks[task_id]["result"] = {"success": True, "path": f"assets/images/{fname}", "type": "image"}
            _gen_tasks[task_id]["status"] = "succeeded"
            return

        elif mode == "video":
            # ----- 视频生成 -----
            _set_task_stage(task_id, "submitting", 3, "正在提交视频生成请求...")
            payload = {
                "model": "agnes-video-v2.0",
                "prompt": prompt,
            }
            if image_path:
                img_full = (project_dir / image_path).resolve()
                try:
                    img_full.relative_to(project_dir.resolve())
                except ValueError:
                    raise RuntimeError("路径越出项目目录")
                import base64
                with open(img_full, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode()
                payload["image"] = f"data:image/png;base64,{img_b64}"

            # 提交任务（503/429 重试）
            _set_task_stage(task_id, "submitting", 5, "提交视频任务到 Agnes...")
            data = None
            for _attempt in range(5):
                try:
                    resp = http_requests.post(f"{base_url}/videos", headers=headers, json=payload, timeout=30)
                    if resp.status_code in (429, 502, 503):
                        retry_after = int(resp.headers.get("Retry-After", "65"))
                        _set_task_stage(task_id, "submitting", 5 + _attempt * 3, f"Agnes 繁忙（HTTP {resp.status_code}），等待 {retry_after}秒后重试（第{_attempt+1}次）...")
                        time.sleep(retry_after)
                        continue
                    resp.raise_for_status()
                    data = resp.json()
                    break
                except Exception as e:
                    if _attempt < 4:
                        _set_task_stage(task_id, "submitting", 5 + _attempt * 3, f"提交异常，重试中（第{_attempt+1}次）: {e}")
                        time.sleep(10)
                    else:
                        raise RuntimeError(f"Agnes 视频 API 提交失败（已重试 5 次）: {e}")
            if data is None:
                raise RuntimeError("Agnes 视频 API 提交失败：未获取到响应")

            video_id = data.get("id") or data.get("video_id")
            if not video_id:
                raise RuntimeError("Agnes API 未返回任务 ID")

            _set_task_stage(task_id, "polling", 10, f"任务已提交（ID: {video_id[:16]}...），等待 Agnes 生成...")

            # 轮询状态（最大 10 分钟）
            max_wait = 600
            waited = 0
            video_url = None
            last_status = ""
            last_progress = 0
            while waited < max_wait:
                time.sleep(5)
                waited += 5
                try:
                    status_resp = http_requests.get(f"{base_url}/videos/{video_id}", headers=headers, timeout=15)
                    if status_resp.status_code in (429, 502, 503):
                        continue
                    status_resp.raise_for_status()
                    status_data = status_resp.json()
                except Exception:
                    continue

                status = status_data.get("status", "")
                # 估算进度：10% (起始) -> 90% (完成前)
                if status in ("queued", "pending"):
                    cur_progress = 10
                    msg = f"排队中... ({waited}s)"
                elif status in ("in_progress", "processing", "running"):
                    cur_progress = min(10 + int(waited / max_wait * 70), 85)
                    p = status_data.get("progress")
                    if isinstance(p, (int, float)) and p > 0:
                        cur_progress = min(10 + int(p * 0.75), 85)
                    msg = f"生成中... {cur_progress}% ({waited}s)"
                elif status in ("succeeded", "complete", "completed"):
                    video_url = (
                        status_data.get("url")
                        or status_data.get("video_url")
                        or status_data.get("metadata", {}).get("url")
                    )
                    cur_progress = 90
                    msg = "生成完成，准备下载..."
                    _set_task_stage(task_id, "polling", cur_progress, msg)
                    break
                elif status in ("failed", "error"):
                    error = status_data.get("error", "未知错误")
                    raise RuntimeError(f"Agnes 视频生成失败: {error}")
                else:
                    cur_progress = 10
                    msg = f"状态: {status} ({waited}s)"

                if cur_progress != last_progress or msg != last_status:
                    _set_task_stage(task_id, "polling", cur_progress, msg)
                    last_progress = cur_progress
                    last_status = msg
            else:
                raise RuntimeError(f"视频生成超时（>{max_wait}秒）")

            if not video_url:
                raise RuntimeError("未获取到视频 URL")

            _set_task_stage(task_id, "downloading", 92, "下载视频文件...")
            fname = f"{hashlib.md5(prompt.encode()).hexdigest()[:10]}_{int(time.time())}.mp4"
            save_path = project_dir / "assets" / "video" / fname
            (project_dir / "assets" / "video").mkdir(parents=True, exist_ok=True)

            vid_resp = http_requests.get(video_url, timeout=180)
            vid_resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(vid_resp.content)

            _invalidate_summary(project_id)
            hub.publish(project_id)
            _set_task_stage(task_id, "done", 100, "视频生成完成")
            _gen_tasks[task_id]["result"] = {"success": True, "path": f"assets/video/{fname}", "type": "video"}
            _gen_tasks[task_id]["status"] = "succeeded"
            return

        else:
            raise RuntimeError(f"不支持的生成模式: {mode}")

    except Exception as e:
        _gen_tasks[task_id]["status"] = "failed"
        _gen_tasks[task_id]["error"] = str(e)
        _set_task_stage(task_id, "failed", 0, f"失败: {e}")


def create_app() -> FastAPI:
    app = FastAPI(title="Backlot", docs_url=None, redoc_url=None)

    @app.on_event("startup")
    async def _startup() -> None:
        app.state.watch_task = asyncio.create_task(_watch_projects())

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        task = getattr(app.state, "watch_task", None)
        if task:
            task.cancel()

    # ---- API ----------------------------------------------------------

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True, "app": "backlot"}

    @app.get("/api/projects")
    async def projects() -> list:
        return await asyncio.to_thread(_cached_summaries)

    # 可用的流水线类型
    _PIPELINE_TYPES = [
        {"id": "cinematic", "name": "电影感短片"},
        {"id": "animated-explainer", "name": "动画讲解"},
        {"id": "talking-head", "name": "口播视频"},
        {"id": "screen-demo", "name": "屏幕演示"},
        {"id": "clip-factory", "name": "短视频工厂"},
        {"id": "podcast-repurpose", "name": "播客再剪辑"},
        {"id": "animation", "name": "动画"},
        {"id": "character-animation", "name": "角色动画"},
        {"id": "hybrid", "name": "混合模式"},
        {"id": "avatar-spokesperson", "name": "虚拟人播报"},
        {"id": "localization-dub", "name": "本地化配音"},
        {"id": "documentary-montage", "name": "纪录片剪辑"},
    ]

    @app.get("/api/pipeline-types")
    async def pipeline_types() -> list:
        return _PIPELINE_TYPES

    @app.post("/api/projects")
    async def create_project(req: CreateProjectRequest) -> dict:
        import re
        from lib.checkpoint import init_project
        # 从标题生成 kebab-case 项目 ID
        raw_id = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '-', req.title.strip()).strip('-').lower()
        if not raw_id:
            raw_id = "untitled"
        # 如果目录已存在，加后缀
        base_id = raw_id
        suffix = 2
        while (PROJECTS_DIR / raw_id).exists():
            raw_id = f"{base_id}-{suffix}"
            suffix += 1
        project_dir = await asyncio.to_thread(
            init_project, raw_id, title=req.title, pipeline_type=req.pipeline_type
        )
        _invalidate_summary(raw_id)
        hub.publish(raw_id)
        return {"project_id": raw_id, "title": req.title, "pipeline_type": req.pipeline_type}

    @app.post("/api/project/{project_id}/generate")
    async def generate_asset(project_id: str, req: GenerateRequest) -> dict:
        """提交生成任务，立即返回 task_id。实际生成在后台线程执行，前端通过 /status 端点轮询进度。"""
        import uuid, threading
        project_dir = _safe_project_dir(project_id)
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="项目不存在")

        api_key = os.environ.get("AGNES_API_KEY", "")
        if not api_key:
            raise HTTPException(status_code=400, detail="未配置 AGNES_API_KEY")

        if req.mode not in ("image", "video"):
            raise HTTPException(status_code=400, detail="不支持的生成模式")

        task_id = f"gen_{uuid.uuid4().hex[:12]}"
        _gen_tasks[task_id] = {
            "status": "pending",
            "stage": "pending",
            "progress": 0,
            "message": "任务已创建，等待启动...",
            "result": None,
            "error": None,
            "project_id": project_id,
            "mode": req.mode,
            "prompt": req.prompt,
            "started_at": time.time(),
        }

        # 启动后台线程执行实际生成（不阻塞事件循环）
        thread = threading.Thread(
            target=_run_gen_task,
            args=(task_id, project_id, req.prompt, req.mode, req.image_path),
            daemon=True,
        )
        thread.start()

        return {"task_id": task_id, "status": "pending", "mode": req.mode}

    @app.get("/api/project/{project_id}/generate/status/{task_id}")
    async def generate_status(project_id: str, task_id: str) -> dict:
        """查询生成任务状态。前端轮询此端点获取进度。"""
        t = _gen_tasks.get(task_id)
        if not t:
            raise HTTPException(status_code=404, detail="任务不存在")
        if t.get("project_id") != project_id:
            raise HTTPException(status_code=404, detail="任务不属于该项目")

        # 清理超过 30 分钟的已完成/已失败任务
        if t["status"] in ("succeeded", "failed") and time.time() - t.get("started_at", 0) > 1800:
            _gen_tasks.pop(task_id, None)
            raise HTTPException(status_code=404, detail="任务已过期")

        resp = {
            "task_id": task_id,
            "status": t["status"],
            "stage": t.get("stage", ""),
            "progress": t.get("progress", 0),
            "message": t.get("message", ""),
            "mode": t.get("mode", ""),
        }
        if t["status"] == "succeeded":
            resp["result"] = t.get("result")
        elif t["status"] == "failed":
            resp["error"] = t.get("error")
        return resp
    @app.get("/api/project/{project_id}/assets")
    async def list_assets(project_id: str) -> dict:
        """列出项目中的所有素材"""
        project_dir = _safe_project_dir(project_id)
        images = []
        videos = []

        img_dir = project_dir / "assets" / "images"
        if img_dir.is_dir():
            for f in sorted(img_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                    images.append({"path": f"assets/images/{f.name}", "name": f.name, "size": f.stat().st_size})

        vid_dir = project_dir / "assets" / "video"
        if vid_dir.is_dir():
            for f in sorted(vid_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in (".mp4", ".webm", ".mov"):
                    videos.append({"path": f"assets/video/{f.name}", "name": f.name, "size": f.stat().st_size})

        return {"images": images, "videos": videos}

    @app.delete("/api/project/{project_id}")
    async def delete_project(project_id: str) -> dict:
        """删除项目目录"""
        import shutil
        project_dir = _safe_project_dir(project_id)
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="项目不存在")
        shutil.rmtree(project_dir, ignore_errors=True)
        _invalidate_summary(project_id)
        hub.publish(project_id)
        return {"ok": True, "deleted": project_id}

    @app.get("/api/project/{project_id}/state")
    async def project_state(project_id: str) -> dict:
        project_dir = _safe_project_dir(project_id)
        return await asyncio.to_thread(load_board_state, project_dir)

    @app.get("/api/project/{project_id}/events")
    async def project_events(project_id: str, request: Request) -> StreamingResponse:
        _safe_project_dir(project_id)  # 404 early for unknown projects

        async def stream():
            q = hub.subscribe(project_id)
            try:
                yield _sse({"type": "hello", "project_id": project_id})
                while True:
                    if await request.is_disconnected():
                        return
                    try:
                        await asyncio.wait_for(q.get(), timeout=SSE_HEARTBEAT_SECONDS)
                    except asyncio.TimeoutError:
                        yield _sse({"type": "heartbeat", "ts": time.time()})
                        continue
                    # Coalesce bursts: drain anything else queued.
                    while not q.empty():
                        try:
                            q.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                    yield _sse({"type": "change", "project_id": project_id})
            finally:
                hub.unsubscribe(q)

        return StreamingResponse(stream(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        })

    @app.get("/api/library/events")
    async def library_events(request: Request) -> StreamingResponse:
        async def stream():
            q = hub.subscribe()
            try:
                yield _sse({"type": "hello"})
                while True:
                    if await request.is_disconnected():
                        return
                    try:
                        changed = await asyncio.wait_for(q.get(), timeout=SSE_HEARTBEAT_SECONDS)
                    except asyncio.TimeoutError:
                        yield _sse({"type": "heartbeat", "ts": time.time()})
                        continue
                    while not q.empty():
                        try:
                            q.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                    yield _sse({"type": "change", "project_id": changed})
            finally:
                hub.unsubscribe(q)

        return StreamingResponse(stream(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        })

    # ---- Thumbnails (downscaled, cached on disk) ------------------------

    @app.get("/thumb/{project_id}/{file_path:path}")
    async def thumb(project_id: str, file_path: str, w: int = 640) -> FileResponse:
        project_dir = _safe_project_dir(project_id)
        target = (project_dir / file_path).resolve()
        try:
            target.relative_to(project_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="路径越出项目目录")
        if not target.is_file():
            raise HTTPException(status_code=404, detail="未找到媒体文件")
        width = min(THUMB_WIDTHS, key=lambda x: abs(x - w))
        cached = await asyncio.to_thread(_thumbnail_for, target, width)
        if cached is None:
            # Never fall back to raw video bytes for an <img> consumer (F-03);
            # non-thumbable images are safe to serve as-is.
            if target.suffix.lower() in {".mp4", ".webm", ".mov"}:
                raise HTTPException(status_code=404, detail="没有可用的封面帧")
            return FileResponse(target)
        return FileResponse(cached, media_type="image/jpeg")

    # ---- Media (range requests handled by FileResponse) ---------------

    @app.get("/media/{project_id}/{file_path:path}")
    async def media(project_id: str, file_path: str) -> FileResponse:
        project_dir = _safe_project_dir(project_id)
        target = (project_dir / file_path).resolve()
        try:
            target.relative_to(project_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="路径越出项目目录")
        if not target.is_file():
            raise HTTPException(status_code=404, detail="未找到媒体文件")
        return FileResponse(target)

    # ---- UI ------------------------------------------------------------

    @app.get("/p/{project_id}")
    async def board_page(project_id: str) -> HTMLResponse:
        return _ui_html("board.html", ("board.css", "board.js"))

    @app.get("/p/{project_path:path}")
    async def board_page_path(project_path: str) -> HTMLResponse:
        return _ui_html("board.html", ("board.css", "board.js"))

    @app.get("/")
    async def library_page() -> HTMLResponse:
        return _ui_html("index.html", ("board.css", "library.js"))

    if UI_DIR.is_dir():
        app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

    # The board is a long-lived SPA: a tab keeps running whatever board.js it
    # loaded, and browsers heuristically cache /ui assets. no-cache forces a
    # conditional revalidation (cheap 304 via ETag) on every load so UI fixes
    # show up on a plain refresh. Media/thumb responses keep normal caching.
    @app.middleware("http")
    async def ui_no_cache(request, call_next):
        response = await call_next(request)
        path = request.url.path
        if path == "/" or path.startswith("/ui") or path.startswith("/p/"):
            response.headers["Cache-Control"] = "no-cache"
        return response

    return app


def _safe_project_dir(project_id: str) -> Path:
    # ':' rejects Windows drive-relative ids like "C:" (PROJECTS_DIR / "C:"
    # collapses back to PROJECTS_DIR itself).
    if any(c in project_id for c in "/\\:") or project_id in (".", ".."):
        raise HTTPException(status_code=400, detail="无效的项目 ID")
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"未知项目：{project_id}")
    return project_dir


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


def _thumbnail_for(source: Path, width: int) -> Optional[Path]:
    """Downscale an image (or extract a video poster frame) to a cached JPEG."""
    suffix = source.suffix.lower()
    is_image = suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    is_video = suffix in {".mp4", ".webm", ".mov"}
    if not (is_image or is_video):
        return None
    try:
        import hashlib
        stat = source.stat()
        key = hashlib.sha1(
            f"{source}|{stat.st_mtime_ns}|{stat.st_size}|{width}".encode()
        ).hexdigest()[:20]
        cached = THUMB_CACHE_DIR / f"{key}.jpg"
        if cached.is_file():
            return cached
        THUMB_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Unique temp per request — concurrent misses for the same source
        # must not write (and replace from) the same temp file.
        import uuid
        tmp = THUMB_CACHE_DIR / f"{key}.{uuid.uuid4().hex[:8]}.tmp.jpg"
        if is_video:
            import subprocess
            result = subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5",
                 "-i", str(source), "-frames:v", "1",
                 "-vf", f"scale={width}:-2", str(tmp)],
                capture_output=True, timeout=30,
            )
            if result.returncode != 0 or not tmp.is_file():
                return None
        else:
            from PIL import Image
            with Image.open(source) as img:
                img = img.convert("RGB")
                img.thumbnail((width, width * 3))
                img.save(tmp, "JPEG", quality=82)
        tmp.replace(cached)
        return cached
    except Exception:
        return None


app = create_app()
