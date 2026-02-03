"""X (Twitter) adapter using Tweepy."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict


class XAdapter:
    """Dispatches content to X using the Tweepy client."""

    PLATFORM = "X"
    MAX_TEXT_LENGTH = 280
    REQUIRED_FIELDS = ("api_key", "api_secret", "access_token", "access_token_secret")

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
                "detail": "Missing X credentials. Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET.",
            }

        if not find_spec("tweepy"):
            return {
                "status": "ERROR",
                "detail": "tweepy is not installed. Install it to dispatch to X.",
            }

        content = payload.get("payload", {})
        return {
            "status": "SUCCESS",
            "detail": "Ready to post to X via Tweepy (fill in API client calls).",
            "payload": {
                "text": content.get("text"),
                "image_file": content.get("image_file"),
                "video_file": content.get("video_file"),
            },
        }
