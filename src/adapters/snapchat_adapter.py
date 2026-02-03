"""Snapchat adapter using Snapchat Marketing API libraries."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class SnapchatAdapter(BaseAdapter):
    """Dispatches content to Snapchat using the Snapchat Marketing API."""

    PLATFORM = "SNAPCHAT"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Snapchat credentials. Set SNAPCHAT_CLIENT_ID, SNAPCHAT_CLIENT_SECRET, SNAPCHAT_ACCESS_TOKEN.",
            )

        if not find_spec("snapchat"):
            return self._result(
                ResultStatus.FAILED,
                "Snapchat SDK is not installed. Install a Snapchat Marketing API SDK to dispatch.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Snapchat dispatch not implemented. Integrate Snapchat Marketing API calls.",
        )
