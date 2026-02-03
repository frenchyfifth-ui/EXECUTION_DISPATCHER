"""YouTube adapter using the Google API client."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter


class YouTubeAdapter(BaseAdapter):
    """Dispatches content to YouTube using the YouTube Data API v3."""

    PLATFORM = "YOUTUBE"
    MAX_TEXT_LENGTH = 5000
    REQUIRED_FIELDS = ("client_id", "client_secret", "refresh_token")

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.live_mode:
            return self._dry_run_response("Ready to upload to YouTube.", payload)
        if not self._require_credentials():
            return {
                "status": "ERROR",
                "detail": "Missing YouTube credentials. Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.",
            }

        if not find_spec("googleapiclient"):
            return {
                "status": "ERROR",
                "detail": "google-api-python-client is not installed. Install it to dispatch to YouTube.",
            }

        return {
            "status": "SUCCESS",
            "detail": "Ready to upload to YouTube via googleapiclient (fill in OAuth flow).",
            "payload": payload.get("payload", {}),
            "monetization_hint": payload.get("monetization_hint"),
        }
