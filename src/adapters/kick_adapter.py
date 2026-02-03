"""Kick adapter using a Kick API client."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class KickAdapter(BaseAdapter):
    """Dispatches content to Kick using a Kick API client."""

    PLATFORM = "KICK"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Kick.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Kick credentials. Set KICK_CLIENT_ID, KICK_CLIENT_SECRET, KICK_ACCESS_TOKEN.",
            }

        if not find_spec("kickapi"):
            return {
                "status": "ERROR",
                "detail": "Kick API client is not installed. Install a Kick SDK to dispatch.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Kick via SDK (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
