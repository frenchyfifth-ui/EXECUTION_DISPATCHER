"""X (Twitter) adapter using Tweepy."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class XAdapter(BaseAdapter):
    """Dispatches content to X using the Tweepy client."""

    PLATFORM = "X"
    MAX_TEXT_LENGTH = 280
    REQUIRED_FIELDS = ("api_key", "api_secret", "access_token", "access_token_secret")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to X.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing X credentials. Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET.",
            }

        if not find_spec("tweepy"):
            return {
                "status": "ERROR",
                "detail": "tweepy is not installed. Install it to dispatch to X.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to X via Tweepy (fill in API client calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
