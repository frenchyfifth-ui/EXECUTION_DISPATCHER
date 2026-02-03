"""Telegram adapter using python-telegram-bot."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class TelegramAdapter(BaseAdapter):
    """Dispatches content to Telegram using python-telegram-bot."""

    PLATFORM = "TELEGRAM"
    MAX_TEXT_LENGTH = 4096
    REQUIRED_FIELDS = ("api_key",)

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Telegram credentials. Set TELEGRAM_API_KEY (bot token).",
            )

        if not find_spec("telegram"):
            return self._result(
                ResultStatus.FAILED,
                "python-telegram-bot is not installed. Install it to dispatch to Telegram.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Telegram dispatch not implemented. Integrate python-telegram-bot calls.",
        )
