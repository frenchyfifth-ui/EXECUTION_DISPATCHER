"""Result models for adapter dispatches."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DispatchResult:
    """Result of a platform dispatch attempt."""

    platform: str
    status: str
    message: str


class ResultStatus:
    """Allowed status values for dispatch results."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
