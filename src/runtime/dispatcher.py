"""Main execution engine for dispatching payloads to multiple platforms."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List

from src.adapters import (
    InstagramAdapter,
    KickAdapter,
    LinkedInAdapter,
    PinterestAdapter,
    SnapchatAdapter,
    TelegramAdapter,
    TikTokAdapter,
    TwitchAdapter,
    XAdapter,
    YouTubeAdapter,
)

LOG_FILE = Path("logs/execution.log")
CANONICAL_DIR = Path("canonical")
NORMALIZED_DIR = Path("normalized")

PLATFORM_ADAPTERS = {
    "YOUTUBE": YouTubeAdapter,
    "X": XAdapter,
    "LINKEDIN": LinkedInAdapter,
    "TIKTOK": TikTokAdapter,
    "INSTAGRAM": InstagramAdapter,
    "TWITCH": TwitchAdapter,
    "SNAPCHAT": SnapchatAdapter,
    "PINTEREST": PinterestAdapter,
    "KICK": KickAdapter,
    "TELEGRAM": TelegramAdapter,
}


def setup_logging() -> logging.Logger:
    """Configure console and file logging."""
    logger = logging.getLogger("execution_dispatcher")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def load_canonical_events() -> List[Path]:
    """Load canonical markdown event files for reference."""
    return sorted(CANONICAL_DIR.glob("*.md"))


def load_normalized_payloads() -> List[Dict[str, Any]]:
    """Load normalized JSON payloads from disk."""
    payloads: List[Dict[str, Any]] = []
    for payload_path in sorted(NORMALIZED_DIR.glob("*.json")):
        with payload_path.open("r", encoding="utf-8") as handle:
            payloads.append(json.load(handle))
    return payloads


def get_credentials(platform: str) -> Dict[str, str | None]:
    """Collect credentials for a platform from environment variables."""
    prefix = platform.upper()
    return {
        "api_key": os.getenv(f"{prefix}_API_KEY"),
        "api_secret": os.getenv(f"{prefix}_API_SECRET"),
        "access_token": os.getenv(f"{prefix}_ACCESS_TOKEN"),
        "access_token_secret": os.getenv(f"{prefix}_ACCESS_TOKEN_SECRET"),
        "refresh_token": os.getenv(f"{prefix}_REFRESH_TOKEN"),
        "client_id": os.getenv(f"{prefix}_CLIENT_ID"),
        "client_secret": os.getenv(f"{prefix}_CLIENT_SECRET"),
    }


def iter_target_platforms(payload: Dict[str, Any]) -> Iterable[str]:
    """Yield normalized platform names."""
    platforms = payload.get("target_platforms", [])
    return [platform.upper() for platform in platforms]


def dispatch_all() -> None:
    """Run the multi-platform dispatch loop."""
    logger = setup_logging()
    canonical_events = load_canonical_events()
    logger.info("Loaded %s canonical events.", len(canonical_events))
    for event_path in canonical_events:
        logger.info("Canonical event loaded: %s", event_path)

    payloads = load_normalized_payloads()
    logger.info("Loaded %s normalized payloads.", len(payloads))

    throttle_seconds = float(os.getenv("DISPATCH_THROTTLE_SECONDS", "0"))

    for payload in payloads:
        event_id = payload.get("event_id", "unknown")
        logger.info("Processing payload %s", event_id)
        for platform in iter_target_platforms(payload):
            adapter_class = PLATFORM_ADAPTERS.get(platform)
            if not adapter_class:
                logger.error("FAILED | Unsupported platform: %s", platform)
                continue

            credentials = get_credentials(platform)
            adapter = adapter_class(credentials=credentials, logger=logger)
            if not adapter.validate(payload):
                logger.error("FAILED | Validation failed for %s", platform)
                continue
            try:
                response = adapter.dispatch(payload)
            except Exception as exc:  # noqa: BLE001 - ensure graceful handling
                logger.error("ERROR | Dispatch error on %s: %s", platform, exc)
            else:
                logger.info("SUCCESS | %s response: %s", platform, response)

            if throttle_seconds > 0:
                logger.info("Throttling for %s seconds", throttle_seconds)
                import time

                time.sleep(throttle_seconds)


if __name__ == "__main__":
    dispatch_all()
