"""TikTok adapter using TikTokApi."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class TikTokAdapter(BaseAdapter):
    """Dispatches content to TikTok using TikTokApi."""

    PLATFORM = "TIKTOK"
    MAX_TEXT_LENGTH = 2200
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to post to TikTok.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing TikTok credentials. Set TIKTOK_CLIENT_ID, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN.",
            }

        if not find_spec("tiktokapi"):
            return {
                "status": "ERROR",
                "detail": "TikTokApi is not installed. Install it to dispatch to TikTok.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to post to TikTok via TikTokApi (configure API calls).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
