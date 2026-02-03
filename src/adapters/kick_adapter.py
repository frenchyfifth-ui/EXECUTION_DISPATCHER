"""Kick adapter using a Kick API client."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class KickAdapter(BaseAdapter):
    """Dispatches content to Kick using a Kick API client."""

    PLATFORM = "KICK"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("client_id", "client_secret", "access_token")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Kick credentials. Set KICK_CLIENT_ID, KICK_CLIENT_SECRET, KICK_ACCESS_TOKEN.",
            )

        if not find_spec("kickapi"):
            return self._result(
                ResultStatus.FAILED,
                "Kick API client is not installed. Install a Kick SDK to dispatch.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Kick dispatch not implemented. Integrate Kick SDK calls.",
        )
