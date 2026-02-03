"""Platform adapters."""

from .youtube_adapter import YouTubeAdapter
from .x_adapter import XAdapter
from .linkedin_adapter import LinkedInAdapter
from .tiktok_adapter import TikTokAdapter
from .instagram_adapter import InstagramAdapter
from .twitch_adapter import TwitchAdapter
from .snapchat_adapter import SnapchatAdapter
from .pinterest_adapter import PinterestAdapter
from .kick_adapter import KickAdapter
from .telegram_adapter import TelegramAdapter

__all__ = [
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
