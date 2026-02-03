"""LinkedIn adapter using linkedin-api."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class LinkedInAdapter(BaseAdapter):
    """Dispatches content to LinkedIn using linkedin-api."""

    PLATFORM = "LINKEDIN"
    MAX_TEXT_LENGTH = 3000
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to LinkedIn.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing LinkedIn credentials. Set LINKEDIN_ACCESS_TOKEN.",
            }

        if not find_spec("linkedin_api"):
            return {
                "status": "ERROR",
                "detail": "linkedin-api is not installed. Install it to dispatch to LinkedIn.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to LinkedIn via linkedin-api (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
