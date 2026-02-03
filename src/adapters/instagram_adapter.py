"""Instagram adapter using instagrapi."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class InstagramAdapter(BaseAdapter):
    """Dispatches content to Instagram using instagrapi."""

    PLATFORM = "INSTAGRAM"
    MAX_TEXT_LENGTH = 2200
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Instagram.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Instagram credentials. Set INSTAGRAM_ACCESS_TOKEN.",
            }

        if not find_spec("instagrapi"):
            return {
                "status": "ERROR",
                "detail": "instagrapi is not installed. Install it to dispatch to Instagram.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Instagram via instagrapi (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
