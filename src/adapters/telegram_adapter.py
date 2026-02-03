"""Telegram adapter using python-telegram-bot."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class TelegramAdapter(BaseAdapter):
    """Dispatches content to Telegram using python-telegram-bot."""

    PLATFORM = "TELEGRAM"
    MAX_TEXT_LENGTH = 4096
    REQUIRED_FIELDS = ("api_key",)

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Telegram.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Telegram credentials. Set TELEGRAM_API_KEY (bot token).",
            }

        if not find_spec("telegram"):
            return {
                "status": "ERROR",
                "detail": "python-telegram-bot is not installed. Install it to dispatch to Telegram.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Telegram via python-telegram-bot (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
