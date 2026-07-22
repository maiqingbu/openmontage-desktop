"""Agnes AI image generation via Agnes API (agnes-image-2.x-flash).

Sapiens AI 旗下的多模态图片模型，支持文生图 / 图生图 / 多图合成。
当前无限期免费。
"""

from __future__ import annotations

import base64
import mimetypes
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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


def _file_to_data_uri(path_str: str) -> str:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"输入文件不存在: {path}")
    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type:
        mime_type = "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _normalize_image_input(url_value: str | None, path_value: str | None) -> str | None:
    if url_value:
        return url_value
    if path_value:
        return _file_to_data_uri(path_value)
    return None


class AgnesImage(BaseTool):
    name = "agnes_image"
    version = "1.0.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "agnes"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set AGNES_API_KEY to your Agnes AI API key.\n"
        "  Get one at https://platform.agnes-ai.com"
    )
    agent_skills = ["ai-image-gen"]

    capabilities = [
        "generate_image",
        "edit_image",
        "text_to_image",
        "image_to_image",
        "multi_image_composite",
    ]
    supports = {
        "image_edit": True,
        "multiple_outputs": False,
        "aspect_ratio": True,
        "resolution": True,
        "reference_image": True,
        "multiple_reference_images": True,
        "multi_image_composite": True,
    }
    best_for = [
        "免费无限图片生成",
        "中文 prompt 图片生成",
        "角色 + 场景多图合成",
        "图生图风格迁移",
    ]
    not_good_for = ["离线生成", "严格像素级图像融合", "超高分辨率（>2K）"]
    fallback_tools = ["flux_image", "openai_image", "google_imagen"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string", "description": "图片描述文本"},
            "generation_mode": {
                "type": "string",
                "enum": ["generate", "edit", "composite"],
                "default": "generate",
                "description": "generate=文生图, edit=图生图, composite=多图合成",
            },
            "model": {
                "type": "string",
                "enum": ["agnes-image-2.0-flash", "agnes-image-2.1-flash"],
                "default": "agnes-image-2.1-flash",
            },
            "size": {
                "type": "string",
                "enum": ["1024x1024", "1152x768", "768x1152", "1280x720", "720x1280"],
                "default": "1024x1024",
                "description": "输出尺寸",
            },
            "image_url": {"type": "string", "description": "图生图/合成的源图 URL"},
            "image_path": {"type": "string", "description": "图生图/合成的本地源图路径"},
            "image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "多图合成的多个源图 URL",
            },
            "image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "多图合成的多个本地源图路径",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=100, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "generation_mode", "model", "size"]
    side_effects = ["写入图片文件到 output_path", "调用 Agnes AI API"]
    user_visible_verification = ["检查生成图片的构图质量和编辑保真度"]

    def _get_api_key(self) -> str | None:
        return os.environ.get("AGNES_API_KEY")

    def _get_base_url(self) -> str:
        return os.environ.get("AGNES_API_BASE_URL", "https://apihub.agnes-ai.com/v1")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0  # Agnes 图片生成当前免费

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        mode = inputs.get("generation_mode", "generate")
        if mode == "composite":
            return 30.0
        return 20.0

    def _build_payload(self, inputs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        base_url = self._get_base_url()
        mode = inputs.get("generation_mode", "generate")
        payload: dict[str, Any] = {
            "model": inputs.get("model", "agnes-image-2.1-flash"),
            "prompt": inputs["prompt"],
            "size": inputs.get("size", "1024x1024"),
        }

        # 收集所有输入图片
        primary_image = _normalize_image_input(inputs.get("image_url"), inputs.get("image_path"))
        extra_images = list(inputs.get("image_urls") or [])
        extra_images.extend(
            _file_to_data_uri(p) for p in (inputs.get("image_paths") or [])
        )

        all_images = []
        if primary_image:
            all_images.append(primary_image)
        all_images.extend(extra_images)

        # 有图片输入时切换到 edit/composite 模式
        if all_images:
            if mode == "generate":
                mode = "composite" if len(all_images) > 1 else "edit"
            payload["image"] = all_images if len(all_images) > 1 else all_images[0]

        endpoint = f"{base_url}/images/generations"
        return endpoint, payload

    @staticmethod
    def _infer_extension(url: str) -> str:
        suffix = Path(urlparse(url).path).suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            return suffix
        return ".png"

    @staticmethod
    def _output_paths(output_path: str | None, count: int, extension: str) -> list[Path]:
        if not output_path:
            stem = "agnes_image"
            return [Path(f"{stem}_{idx + 1}{extension}") for idx in range(count)]

        path = Path(output_path)
        suffix = path.suffix or extension
        if count == 1:
            return [path if path.suffix else path.with_suffix(suffix)]

        base = path.with_suffix("") if path.suffix else path
        return [base.parent / f"{base.name}_{idx + 1}{suffix}" for idx in range(count)]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="AGNES_API_KEY 未设置。" + self.install_instructions,
            )

        import requests

        start = time.time()
        try:
            endpoint, payload = self._build_payload(inputs)
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            data = response.json()

            items = data.get("data", [])
            if not items:
                return ToolResult(success=False, error="Agnes API 未返回图片输出")

            extension = ".png"
            first_url = items[0].get("url")
            if first_url:
                extension = self._infer_extension(first_url)

            output_paths = self._output_paths(inputs.get("output_path"), len(items), extension)
            artifacts: list[str] = []
            outputs: list[str] = []

            for item, output_path in zip(items, output_paths):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                if item.get("b64_json"):
                    output_path.write_bytes(base64.b64decode(item["b64_json"]))
                else:
                    image_url = item.get("url")
                    if not image_url:
                        return ToolResult(success=False, error="Agnes 图片输出缺少 url")
                    download = requests.get(image_url, timeout=120)
                    download.raise_for_status()
                    output_path.write_bytes(download.content)
                artifacts.append(str(output_path))
                outputs.append(str(output_path))

        except requests.exceptions.HTTPError as e:
            return ToolResult(
                success=False,
                error=f"Agnes API HTTP 错误: {e.response.status_code} - {e.response.text[:500]}",
            )
        except Exception as e:
            return ToolResult(success=False, error=f"Agnes 图片生成失败: {e}")

        primary_output = outputs[0]
        return ToolResult(
            success=True,
            data={
                "provider": "agnes",
                "model": payload["model"],
                "prompt": inputs["prompt"],
                "generation_mode": inputs.get("generation_mode", "generate"),
                "output": primary_output,
                "outputs": outputs,
                "images_generated": len(outputs),
            },
            artifacts=artifacts,
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=payload["model"],
        )
