"""ImageGenerationTool — generates campaign images via configurable provider."""

from __future__ import annotations

import base64
import io
from pathlib import Path

import httpx
from infrastructure.config.settings import get_settings
from infrastructure.logging.logger import get_logger


class ImageGenerationTool:
    """Tool (not agent) that generates images from visual prompts."""

    name = "image_generation"

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger(self.name)
        self._output_dir = Path("outputs/images")
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def generate(self, prompt: str, campaign_id: str = "default") -> dict:
        """Generate an image from a cinematic prompt and save to disk."""
        self.logger.info(f"Generating image for campaign {campaign_id}")
        url = self.settings.image_api_url.rstrip("/")
        api_key = self.settings.image_api_key
        model = self.settings.image_model

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
        }

        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                resp = await client.post(
                    f"{url}/images/generations",
                    headers=headers,
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()

            # OpenAI-compatible response: data[0].url or data[0].b64_json
            img_data = data.get("data", [{}])[0]
            img_url = img_data.get("url")
            b64 = img_data.get("b64_json")

            save_path = self._output_dir / f"{campaign_id}.png"

            if b64:
                img_bytes = base64.b64decode(b64)
                save_path.write_bytes(img_bytes)
            elif img_url:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    img_resp = await client.get(img_url)
                    img_resp.raise_for_status()
                    save_path.write_bytes(img_resp.content)
            else:
                self.logger.warning("No image data returned from provider")
                return {"generated_image_path": "", "error": "No image data returned"}

            self.logger.info(f"Image saved to {save_path}")
            return {"generated_image_path": str(save_path), "current_agent": self.name}

        except Exception as exc:
            self.logger.error(f"Image generation failed: {exc}")
            return {"generated_image_path": "", "error": str(exc)}
