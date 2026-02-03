"""Pinterest adapter using the Pinterest API SDK."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class PinterestAdapter(BaseAdapter):
    """Dispatches content to Pinterest using the Pinterest API."""

    PLATFORM = "PINTEREST"
    MAX_TEXT_LENGTH = 500
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Pinterest credentials. Set PINTEREST_ACCESS_TOKEN.",
            )

        if not find_spec("pinterest"):
            return self._result(
                ResultStatus.FAILED,
                "Pinterest SDK is not installed. Install it to dispatch to Pinterest.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Pinterest dispatch not implemented. Integrate Pinterest SDK calls.",
        )
