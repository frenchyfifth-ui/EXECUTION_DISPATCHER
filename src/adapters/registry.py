"""Adapter registry for platform resolution."""

from __future__ import annotations

from typing import Dict, Type

from src.adapters.base import BaseAdapter

_REGISTRY: Dict[str, Type[BaseAdapter]] = {}


def register_adapter(adapter_class: Type[BaseAdapter]) -> None:
    """Register an adapter for its platform key."""
    platform = adapter_class.PLATFORM.upper()
    _REGISTRY[platform] = adapter_class


def resolve_adapter(platform: str) -> Type[BaseAdapter] | None:
    """Resolve a platform name to an adapter class."""
    return _REGISTRY.get(platform.upper())


def registered_platforms() -> Dict[str, Type[BaseAdapter]]:
    """Return a copy of the registry."""
    return dict(_REGISTRY)
