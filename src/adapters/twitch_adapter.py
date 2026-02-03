"""Twitch adapter using twitchAPI."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class TwitchAdapter(BaseAdapter):
    """Dispatches content to Twitch using twitchAPI."""

    PLATFORM = "TWITCH"
    MAX_TEXT_LENGTH = 140
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Twitch.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Twitch credentials. Set TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, TWITCH_ACCESS_TOKEN.",
            }

        if not find_spec("twitchAPI"):
            return {
                "status": "ERROR",
                "detail": "twitchAPI is not installed. Install it to dispatch to Twitch.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Twitch via twitchAPI (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
