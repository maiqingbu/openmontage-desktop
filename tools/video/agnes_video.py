"""Agnes AI video generation via Agnes API (agnes-video-v2.0).

Sapiens AI 旗下的多模态视频模型，支持文生视频 / 图生视频 / 关键帧动画。
当前推广期 $0/秒，标准价 $0.005/秒。
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class AgnesVideo(BaseTool):
    name = "agnes_video"
    version = "1.0.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "agnes"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set AGNES_API_KEY to your Agnes AI API key.\n"
        "  Get one at https://agnes-ai.com (developer console)"
    )
    agent_skills = ["ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "keyframes_animation"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "keyframes_animation": True,
        "camera_direction": True,
        "negative_prompt": True,
        "seed_reproducibility": True,
    }
    best_for = [
        "免费推广期视频生成（$0/秒）",
        "中文 prompt 视频生成",
        "图生视频 + 关键帧动画",
        "OpenAI 兼容接口，易迁移",
    ]
    not_good_for = ["离线生成", "超长视频（>18秒）", "需要音频同步的场景"]
    fallback_tools = ["kling_video", "minimax_video", "wan_video"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string", "description": "视频内容文本描述"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "keyframes_animation"],
                "default": "text_to_video",
            },
            "image_url": {
                "type": "string",
                "description": "图生视频的参考图 URL",
            },
            "keyframe_images": {
                "type": "array",
                "items": {"type": "string"},
                "description": "关键帧模式的图片 URL 数组",
            },
            "width": {
                "type": "integer",
                "default": 1152,
                "description": "视频宽度（480p/720p/1080p 对应档位）",
            },
            "height": {
                "type": "integer",
                "default": 768,
                "description": "视频高度",
            },
            "num_frames": {
                "type": "integer",
                "default": 121,
                "description": "帧数，必须 ≤441 且遵循 8n+1 规则（81/121/241/441）",
            },
            "frame_rate": {
                "type": "number",
                "default": 24,
                "description": "帧率 1-60",
            },
            "seed": {
                "type": "integer",
                "description": "随机种子，用于可复现结果",
            },
            "negative_prompt": {
                "type": "string",
                "description": "反向提示词，描述要避免的内容",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout", "503"])
    idempotency_key_fields = ["prompt", "operation", "seed"]
    side_effects = ["写入视频文件到 output_path", "调用 Agnes AI API"]
    user_visible_verification = ["观看生成的视频，检查运动连贯性和 prompt 匹配度"]

    def _get_api_key(self) -> str | None:
        return os.environ.get("AGNES_API_KEY")

    def _get_base_url(self) -> str:
        return os.environ.get("AGNES_API_BASE_URL", "https://apihub.agnes-ai.com/v1")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        num_frames = inputs.get("num_frames", 121)
        frame_rate = inputs.get("frame_rate", 24)
        duration = num_frames / frame_rate if frame_rate > 0 else 5.0
        return 0.0  # 当前推广期 $0/秒，标准价 $0.005/秒

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        num_frames = inputs.get("num_frames", 121)
        if num_frames <= 81:
            return 45.0
        if num_frames <= 121:
            return 90.0
        if num_frames <= 241:
            return 180.0
        return 300.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="AGNES_API_KEY 未设置。" + self.install_instructions,
            )

        import requests

        start = time.time()
        operation = inputs.get("operation", "text_to_video")
        base_url = self._get_base_url()

        payload: dict[str, Any] = {
            "model": "agnes-video-v2.0",
            "prompt": inputs["prompt"],
            "width": inputs.get("width", 1152),
            "height": inputs.get("height", 768),
            "num_frames": inputs.get("num_frames", 121),
            "frame_rate": inputs.get("frame_rate", 24),
        }

        if inputs.get("seed") is not None:
            payload["seed"] = inputs["seed"]
        if inputs.get("negative_prompt"):
            payload["negative_prompt"] = inputs["negative_prompt"]

        if operation == "image_to_video":
            if not inputs.get("image_url"):
                return ToolResult(
                    success=False,
                    error="image_to_video 模式需要提供 image_url 参数",
                )
            payload["image"] = inputs["image_url"]
            payload["mode"] = "ti2vid"
        elif operation == "keyframes_animation":
            keyframes = inputs.get("keyframe_images") or []
            if not keyframes:
                return ToolResult(
                    success=False,
                    error="keyframes_animation 模式需要提供 keyframe_images 数组",
                )
            payload["extra_body"] = {
                "mode": "keyframes",
                "image": keyframes,
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            submit_resp = requests.post(
                f"{base_url}/videos",
                headers=headers,
                json=payload,
                timeout=30,
            )
            submit_resp.raise_for_status()
            task_data = submit_resp.json()
            video_id = task_data.get("video_id") or task_data.get("id")

            if not video_id:
                return ToolResult(
                    success=False,
                    error=f"Agnes API 响应中缺少 video_id: {task_data}",
                )

            max_poll_seconds = 600
            poll_start = time.time()
            poll_interval = 5

            while True:
                if time.time() - poll_start > max_poll_seconds:
                    return ToolResult(
                        success=False,
                        error=f"Agnes 视频生成超时（>{max_poll_seconds}秒），任务 ID: {video_id}",
                    )

                time.sleep(poll_interval)
                status_resp = requests.get(
                    f"{base_url}/videos/{video_id}",
                    headers=headers,
                    timeout=15,
                )
                status_resp.raise_for_status()
                status_data = status_resp.json()
                status = status_data.get("status", "unknown")

                if status == "completed":
                    break
                if status == "failed":
                    error_msg = status_data.get("error") or "未知错误"
                    return ToolResult(
                        success=False,
                        error=f"Agnes 视频生成失败: {error_msg}",
                    )

            video_url = status_data.get("metadata", {}).get("url")
            if not video_url:
                return ToolResult(
                    success=False,
                    error=f"Agnes API 完成响应中缺少 metadata.url: {status_data}",
                )

            video_response = requests.get(video_url, timeout=180)
            video_response.raise_for_status()

            output_path = Path(inputs.get("output_path", "agnes_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_response.content)

        except requests.exceptions.HTTPError as e:
            return ToolResult(
                success=False,
                error=f"Agnes API HTTP 错误: {e.response.status_code} - {e.response.text[:500]}",
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Agnes 视频生成失败: {e}")

        return ToolResult(
            success=True,
            data={
                "provider": "agnes",
                "model": "agnes-video-v2.0",
                "prompt": inputs["prompt"],
                "operation": operation,
                "video_id": video_id,
                "output": str(output_path),
                "size": status_data.get("size"),
                "seconds": status_data.get("seconds"),
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model="agnes-video-v2.0",
        )
