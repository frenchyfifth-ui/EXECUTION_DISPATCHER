"""Twitch adapter using twitchAPI."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class TwitchAdapter(BaseAdapter):
    """Dispatches content to Twitch using twitchAPI."""

    PLATFORM = "TWITCH"
    MAX_TEXT_LENGTH = 140
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Twitch credentials. Set TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, TWITCH_ACCESS_TOKEN.",
            )

        if not find_spec("twitchAPI"):
            return self._result(
                ResultStatus.FAILED,
                "twitchAPI is not installed. Install it to dispatch to Twitch.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Twitch dispatch not implemented. Integrate twitchAPI client calls.",
        )
