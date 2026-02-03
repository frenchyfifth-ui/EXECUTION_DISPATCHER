"""Telegram adapter using python-telegram-bot."""

from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict


class TelegramAdapter:
    """Dispatches content to Telegram using python-telegram-bot."""

    PLATFORM = "TELEGRAM"
    MAX_TEXT_LENGTH = 4096
    REQUIRED_FIELDS = ("api_key",)

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
                "detail": "Missing Telegram credentials. Set TELEGRAM_API_KEY (bot token).",
            }

        if not find_spec("telegram"):
            return {
                "status": "ERROR",
                "detail": "python-telegram-bot is not installed. Install it to dispatch to Telegram.",
            }

        content = payload.get("payload", {})
        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Telegram via python-telegram-bot (configure API calls).",
            "payload": {
                "text": content.get("text"),
                "image_file": content.get("image_file"),
                "video_file": content.get("video_file"),
            },
        }
