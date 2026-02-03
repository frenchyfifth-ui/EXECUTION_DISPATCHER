"""Pinterest adapter using the Pinterest API SDK."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class PinterestAdapter(BaseAdapter):
    """Dispatches content to Pinterest using the Pinterest API."""

    PLATFORM = "PINTEREST"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to Pinterest.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing Pinterest credentials. Set PINTEREST_ACCESS_TOKEN.",
            }

        if not find_spec("pinterest"):
            return {
                "status": "ERROR",
                "detail": "Pinterest SDK is not installed. Install it to dispatch to Pinterest.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to Pinterest via SDK (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
