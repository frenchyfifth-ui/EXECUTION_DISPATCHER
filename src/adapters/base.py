"""Shared adapter utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from src.runtime.results import DispatchResult, ResultStatus

class BaseAdapter(ABC):
    """Base adapter with shared validation and credential handling."""

    PLATFORM: str = ""
    MAX_TEXT_LENGTH: int = 0
    REQUIRED_FIELDS: Tuple[str, ...] = ()
    MEDIA_KEYS: Tuple[str, ...] = ("image_file", "video_file", "audio_file")
    REQUIRE_TEXT: bool = False

    def __init__(self, credentials: Dict[str, str | None], logger, live_mode: bool) -> None:
        self.credentials = credentials
        self.logger = logger
        self.live_mode = live_mode

    def validate(self, payload: Dict[str, Any]) -> bool:
        content = payload.get("payload", {})
        text = str(content.get("text", "")).strip()
        has_media = any(content.get(key) for key in self.MEDIA_KEYS)
        if self.REQUIRE_TEXT and not text:
            self.logger.error("ERROR | %s requires text content.", self.PLATFORM)
            return False
        if not text and not has_media:
            self.logger.error("ERROR | %s requires text or media content.", self.PLATFORM)
            return False
        if self.MAX_TEXT_LENGTH and len(text) > self.MAX_TEXT_LENGTH:
            self.logger.error("ERROR | %s text exceeds limit.", self.PLATFORM)
            return False
        return self._validate_media(content, self.MEDIA_KEYS)

    def _validate_media(self, content: Dict[str, Any], keys: Iterable[str]) -> bool:
        for key in keys:
            media_path = content.get(key)
            if media_path and not Path(media_path).exists():
                self.logger.error("ERROR | %s missing media file: %s", self.PLATFORM, media_path)
                return False
        return True

    def _missing_credentials(self) -> Tuple[str, ...]:
        return tuple(field for field in self.REQUIRED_FIELDS if not self.credentials.get(field))

    def _require_credentials(self) -> bool:
        missing = self._missing_credentials()
        if missing:
            self.logger.error("ERROR | %s missing credentials: %s", self.PLATFORM, ", ".join(missing))
            return False
        return True

    def _result(self, status: str, message: str) -> DispatchResult:
        return DispatchResult(platform=self.PLATFORM, status=status, message=message)

    @abstractmethod
    def dispatch(self, payload: Dict[str, Any]) -> DispatchResult:
        """Dispatch content to the target platform."""
        raise NotImplementedError
