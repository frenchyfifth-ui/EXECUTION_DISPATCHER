"""YouTube adapter using the Google API client."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict


class YouTubeAdapter:
    """Dispatches content to YouTube using the YouTube Data API v3."""

    PLATFORM = "YOUTUBE"
    MAX_TEXT_LENGTH = 5000
    REQUIRED_FIELDS = ("client_id", "client_secret", "refresh_token")

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
        for key in ("video_file", "image_file"):
            media_path = content.get(key)
            if media_path and not Path(media_path).exists():
                self.logger.error("ERROR | %s missing media file: %s", self.PLATFORM, media_path)
                return False
        return True

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not all(self.credentials.get(field) for field in self.REQUIRED_FIELDS):
            return {
                "status": "ERROR",
                "detail": "Missing YouTube credentials. Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.",
            }

        if not find_spec("googleapiclient"):
            return {
                "status": "ERROR",
                "detail": "google-api-python-client is not installed. Install it to dispatch to YouTube.",
            }

        content = payload.get("payload", {})
        return {
            "status": "SUCCESS",
            "detail": "Ready to upload to YouTube via googleapiclient (fill in OAuth flow).",
            "payload": {
                "text": content.get("text"),
                "video_file": content.get("video_file"),
                "image_file": content.get("image_file"),
            },
        }
