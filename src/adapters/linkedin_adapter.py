"""LinkedIn adapter using linkedin-api."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class LinkedInAdapter(BaseAdapter):
    """Dispatches content to LinkedIn using linkedin-api."""

    PLATFORM = "LINKEDIN"
    MAX_TEXT_LENGTH = 3000
    REQUIRED_FIELDS = ("access_token",)

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing LinkedIn credentials. Set LINKEDIN_ACCESS_TOKEN.",
            )

        if not find_spec("linkedin_api"):
            return self._result(
                ResultStatus.FAILED,
                "linkedin-api is not installed. Install it to dispatch to LinkedIn.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "LinkedIn dispatch not implemented. Integrate linkedin-api calls.",
        )
