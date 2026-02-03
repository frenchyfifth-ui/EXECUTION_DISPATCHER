"""Data models for execution events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ContentPayload:
    """Normalized content payload."""

    text: str
    image_file: Optional[str] = None
    video_file: Optional[str] = None
    audio_file: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ContentPayload":
        text = str(payload.get("text", "")).strip()
        return cls(
            text=text,
            image_file=payload.get("image_file"),
            video_file=payload.get("video_file"),
            audio_file=payload.get("audio_file"),
        )

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "text": self.text,
            "image_file": self.image_file,
            "video_file": self.video_file,
            "audio_file": self.audio_file,
        }


@dataclass(frozen=True)
class ExecutionEvent:
    """Represents a single execution event."""

    event_id: str
    intent: str
    payload: ContentPayload
    target_platforms: List[str] = field(default_factory=list)
    simultaneity_window: Optional[str] = None
    monetization_hint: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionEvent":
        payload = ContentPayload.from_dict(data.get("payload", {}))
        return cls(
            event_id=str(data.get("event_id", "unknown")),
            intent=str(data.get("intent", "")),
            payload=payload,
            target_platforms=list(data.get("target_platforms", [])),
            simultaneity_window=data.get("simultaneity_window"),
            monetization_hint=data.get("monetization_hint"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "intent": self.intent,
            "payload": self.payload.to_dict(),
            "target_platforms": self.target_platforms,
            "simultaneity_window": self.simultaneity_window,
            "monetization_hint": self.monetization_hint,
        }
