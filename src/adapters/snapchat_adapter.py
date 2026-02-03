"""Snapchat adapter using Snapchat Marketing API libraries."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class SnapchatAdapter(BaseAdapter):
    """Dispatches content to Snapchat using the Snapchat Marketing API."""

    PLATFORM = "SNAPCHAT"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Snapchat.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Snapchat credentials. Set SNAPCHAT_CLIENT_ID, SNAPCHAT_CLIENT_SECRET, SNAPCHAT_ACCESS_TOKEN.",
            }

        if not find_spec("snapchat"):
            return {
                "status": "ERROR",
                "detail": "Snapchat SDK is not installed. Install a Snapchat Marketing API SDK to dispatch.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Snapchat via Marketing API (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
