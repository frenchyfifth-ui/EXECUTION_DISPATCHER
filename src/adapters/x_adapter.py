"""X (Twitter) adapter using Tweepy."""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any, Dict

from src.adapters.base import BaseAdapter
from src.runtime.results import ResultStatus


class XAdapter(BaseAdapter):
    """Dispatches content to X using the Tweepy client."""

    PLATFORM = "X"
    MAX_TEXT_LENGTH = 280
    REQUIRED_FIELDS = ("api_key", "api_secret", "access_token", "access_token_secret")

    def dispatch(self, payload: Dict[str, Any]):
        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing X credentials. Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET.",
            )

        if not find_spec("tweepy"):
            return self._result(
                ResultStatus.FAILED,
                "tweepy is not installed. Install it to dispatch to X.",
            )

        return self._result(
            ResultStatus.NOT_IMPLEMENTED,
            "X dispatch not implemented. Integrate Tweepy client calls.",
        )
