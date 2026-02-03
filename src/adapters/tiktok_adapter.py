"""TikTok adapter using TikTokApi."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict


class TikTokAdapter:
    """Dispatches content to TikTok using TikTokApi."""

    PLATFORM = "TIKTOK"
    MAX_TEXT_LENGTH = 2200
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def __init__(self, credentials: Dict[str, str | None], logger) -> None:
        self.credentials = credentials
        self.logger = logger

    def validate(self, payload: Dict[str, Any]) -> bool:
        content = payload.get("payload", {})
        text = content.get("text", "")
        if not text:
            self.logger.error("ERROR | %s requires text content.", self.PLATFORM)
            return False
        if len(text) > self.MAX_TEXT_LENGTH:
            self.logger.error("ERROR | %s text exceeds limit.", self.PLATFORM)
            return False
        media_path = content.get("video_file")
        if media_path and not Path(media_path).exists():
            self.logger.error("ERROR | %s missing media file: %s", self.PLATFORM, media_path)
            return False
        return True

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not all(self.credentials.get(field) for field in self.REQUIRED_FIELDS):
            return {
                "status": "ERROR",
                "detail": "Missing TikTok credentials. Set TIKTOK_CLIENT_ID, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN.",
            }

        if not find_spec("tiktokapi"):
            return {
                "status": "ERROR",
                "detail": "TikTokApi is not installed. Install it to dispatch to TikTok.",
            }

        content = payload.get("payload", {})
        return {
            "status": "SUCCESS",
            "detail": "Ready to post to TikTok via TikTokApi (configure API calls).",
            "payload": {
                "text": content.get("text"),
                "video_file": content.get("video_file"),
            },
        }
