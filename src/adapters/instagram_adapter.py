"""Instagram adapter using instagrapi."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class InstagramAdapter(BaseAdapter):
    """Dispatches content to Instagram using instagrapi."""

    PLATFORM = "INSTAGRAM"
    MAX_TEXT_LENGTH = 2200
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing Instagram credentials. Set INSTAGRAM_ACCESS_TOKEN.",
            )

        if not find_spec("instagrapi"):
            return self._result(
                ResultStatus.FAILED,
                "instagrapi is not installed. Install it to dispatch to Instagram.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "Instagram dispatch not implemented. Integrate instagrapi client calls.",
        )
