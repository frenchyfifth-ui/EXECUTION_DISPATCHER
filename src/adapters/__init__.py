"""Platform adapters."""

from .base import BaseAdapter
from .instagram_adapter import InstagramAdapter
from .kick_adapter import KickAdapter
from .linkedin_adapter import LinkedInAdapter
from .pinterest_adapter import PinterestAdapter
from .registry import register_adapter
from .snapchat_adapter import SnapchatAdapter
from .telegram_adapter import TelegramAdapter
from .tiktok_adapter import TikTokAdapter
from .twitch_adapter import TwitchAdapter
from .x_adapter import XAdapter
from .youtube_adapter import YouTubeAdapter

__all__ = [
    "BaseAdapter",
    "YouTubeAdapter",
    "XAdapter",
    "LinkedInAdapter",
    "TikTokAdapter",
    "InstagramAdapter",
    "TwitchAdapter",
    "SnapchatAdapter",
    "PinterestAdapter",
    "KickAdapter",
    "TelegramAdapter",
]

for adapter_class in (
    YouTubeAdapter,
    XAdapter,
    LinkedInAdapter,
    TikTokAdapter,
    InstagramAdapter,
    TwitchAdapter,
    SnapchatAdapter,
    PinterestAdapter,
    KickAdapter,
    TelegramAdapter,
):
    register_adapter(adapter_class)
