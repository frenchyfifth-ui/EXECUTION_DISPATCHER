"""TikTok adapter using TikTokApi."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class TikTokAdapter(BaseAdapter):
    """Dispatches content to TikTok using TikTokApi."""

    PLATFORM = "TIKTOK"
    MAX_TEXT_LENGTH = 2200
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing TikTok credentials. Set TIKTOK_CLIENT_ID, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN.",
            )

        if not find_spec("tiktokapi"):
            return self._result(
                ResultStatus.FAILED,
                "TikTokApi is not installed. Install it to dispatch to TikTok.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "TikTok dispatch not implemented. Integrate TikTokApi client calls.",
        )
