"""YouTube adapter using the Google API client."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class YouTubeAdapter(BaseAdapter):
    """Dispatches content to YouTube using the YouTube Data API v3."""

    PLATFORM = "YOUTUBE"
    MAX_TEXT_LENGTH = 5000
    REQUIRED_FIELDS = ("client_id", "client_secret", "refresh_token")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing YouTube credentials. Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.",
            )

        if not find_spec("googleapiclient"):
            return self._result(
                ResultStatus.FAILED,
                "google-api-python-client is not installed. Install it to dispatch to YouTube.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "YouTube dispatch not implemented. Integrate googleapiclient upload flow.",
        )
