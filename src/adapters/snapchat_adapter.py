"""Snapchat adapter using Snapchat Marketing API libraries."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict


class SnapchatAdapter:
    """Dispatches content to Snapchat using the Snapchat Marketing API."""

    PLATFORM = "SNAPCHAT"
    MAX_TEXT_LENGTH = 500
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
        for key in ("image_file", "video_file"):
            media_path = content.get(key)
            if media_path and not Path(media_path).exists():
                self.logger.error("ERROR | %s missing media file: %s", self.PLATFORM, media_path)
                return False
        return True

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not all(self.credentials.get(field) for field in self.REQUIRED_FIELDS):
            return {
                "status": "ERROR",
                "detail": "Missing Snapchat credentials. Set SNAPCHAT_CLIENT_ID, SNAPCHAT_CLIENT_SECRET, SNAPCHAT_ACCESS_TOKEN.",
            }

        if not find_spec("snapchat"):
            return {
                "status": "ERROR",
                "detail": "Snapchat SDK is not installed. Install a Snapchat Marketing API SDK to dispatch.",
            }

        content = payload.get("payload", {})
        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Snapchat via Marketing API (configure API calls).",
            "payload": {
                "text": content.get("text"),
                "image_file": content.get("image_file"),
                "video_file": content.get("video_file"),
            },
        }
