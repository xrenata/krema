"""
Models for guild and other related stuff.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union
from ..errors.guild import *


@dataclass
class Guild:
    """Guild class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes are same with https://discord.com/developers/docs/resources/guild#guild-object-guild-structure
    """

    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        from .user import Member
        from .channel import Channel

        self.client = client

        self.id: int = int(data.get("id"))
        self.name: str = data.get("name")
        self.icon: Union[str, None] = data.get("icon")
        self.icon_hash: Union[str, None] = data.get("icon_hash")
        self.splash: Union[str, None] = data.get("splash")
        self.discovery_splash: Union[str, None] = data.get("discovery_splash")
        self.owner: Union[bool, None] = data.get("owner")
        self.owner_id: Union[int, None] = int(
            data.get("owner_id")) if data.get("owner_id") is not None else None
        self.permissions: Union[str, None] = data.get("permissions")
        self.region: Union[str, None] = data.get("region")
        self.afk_channel_id: Union[int, None] = int(
            data.get("afk_channel_id")) if data.get("afk_channel_id") is not None else None
        self.afk_timeout: int = data.get("afk_timeout")
        self.widget_enabled: Union[bool, None] = data.get("widget_enabled")
        self.widget_channel_id: Union[int, None] = int(
            data.get("widget_channel_id")) if data.get("widget_channel_id") is not None else None
        self.verification_level: int = data.get("verification_level")
        self.default_message_notifications: int = data.get(
            "default_message_notifications")
        self.explicit_content_filter: int = data.get("explicit_content_filter")
        self.roles: list = data.get("roles")
        self.emojis: list = data.get("emojis")
        self.features: list = data.get("features")
        self.mfa_level: int = data.get("mfa_level")
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") is not None else None
        self.system_channel_id: Union[int, None] = int(
            data.get("system_channel_id")) if data.get("system_channel_id") is not None else None
        self.system_channel_flags: Union[int, None] = data.get(
            "system_channel_flags")
        self.rules_channel_id: Union[int, None] = int(
            data.get("rules_channel_id")) if data.get("rules_channel_id") is not None else None
        self.joined_at: Union[datetime, None] = convert_iso(
            data.get("joined_at")) if data.get("joined_at") is not None else None
        self.large: Union[bool, None] = data.get("large")
        self.unavailable: Union[bool, None] = data.get("unavailable")
        self.member_count: Union[int, None] = data.get("member_count")
        self.voice_states: Union[list, None] = data.get("voice_states")
        self.members: Union[list, None] = [Member(self.client, i) for i in data.get(
            "members")] if data.get("members") is not None else None
        self.channels: Union[list, None] = [Channel(self.client, i) for i in data.get(
            "channels")] if data.get("channels") is not None else None
        self.threads: Union[list, None] = [Channel(self.client, i) for i in data.get(
            "threads")] if data.get("threads") is not None else None
        self.presences: Union[list, None] = data.get("presences")
        self.max_presences: Union[int, None] = data.get("max_presences")
        self.max_members: Union[int, None] = data.get("max_members")
        self.vanity_url_code: Union[str, None] = data.get("vanity_url_code")
        self.description: Union[str, None] = data.get("description")
        self.banner: Union[str, None] = data.get("banner")
        self.premium_tier: int = data.get("premium_tier")
        self.premium_subscription_count: Union[int, None] = data.get(
            "premium_subscription_count")
        self.preferred_locale: str = data.get("preferred_locale")
        self.public_updates_channel_id: Union[int, None] = int(data.get(
            "public_updates_channel_id")) if data.get("public_updates_channel_id") is not None else None
        self.max_video_channel_users: Union[int, None] = data.get(
            "max_video_channel_users")
        self.approximate_member_count: Union[int, None] = data.get(
            "approximate_member_count")
        self.approximate_presence_count: Union[int, None] = data.get(
            "approximate_presence_count")
        self.welcome_screen: Union[dict, None] = data.get("welcome_screen")
        self.nsfw_level: int = data.get("nsfw_level")
        self.stage_instances: Union[list, None] = data.get("stage_instances")

    async def fetch_emojis(self):
        """Fetch all emojis in the Guild.

        Returns:
            list: List of Emoji objects.

        Raises:
            FetchEmojisFailed: Fetching the emojis is failed.
        """

        atom, result = await self.client.http.request("GET", f"/guilds/{self.id}/emojis")

        if atom == 0:
            return [Emoji(self.client, i) for i in result]
        else:
            raise FetchEmojisFailed(result)

    async def fetch_emoji(self, emoji_id: int):
        """Fetch a emoji from Guild.

        Args:
            emoji_id (int): Emoji ID.

        Returns:
            Emoji: Found emoji object.

        Raises:
            FetchEmojiFailed: Fetching the emojis is failed.
        """

        atom, result = await self.client.http.request("GET", f"/guilds/{self.id}/emojis/{emoji_id}")

        if atom == 0:
            return Emoji(self.client, result)
        else:
            raise FetchEmojiFailed(result)

    async def create_emoji(self, **kwargs):
        """Create a Guild emoji.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/emoji#create-guild-emoji-json-params (for image, use `krema.utils.image_to_data_uri` function.)

        Returns:
            Emoji: Created Emoji object.

        Raises:
            CreateEmojiFailed: Creating the guild emoji is failed.
        """

        atom, result = await self.client.http.request("POST", f"/guilds/{self.id}/emojis", json=kwargs)

        if atom == 0:
            return Emoji(self.client, result)
        else:
            raise CreateEmojiFailed(result)

    async def update_emoji(self, emoji_id: int, **kwargs):
        """Update a Guild emoji.

        Args:
            emoji_id (int): Emoji ID.
            **kwargs: https://discord.com/developers/docs/resources/emoji#modify-guild-emoji-json-params

        Returns:
            Emoji: Updated Emoji object.

        Raises:
            UpdateEmojiFailed: Updating the guild emoji is failed.
        """

        atom, result = await self.client.http.request("PATCH", f"/guilds/{self.id}/emojis/{emoji_id}", json=kwargs)

        if atom == 0:
            return Emoji(self.client, result)
        else:
            raise UpdateEmojiFailed(result)

    async def delete_emoji(self, emoji_id: int):
        """Delete a Guild emoji.

        Args:
            emoji_id (int): Emoji ID.

        Returns:
            True: Emoji deleted successfully.

        Raises:
            DeleteEmojiFailed: Deleting the guild emoji is failed.
        """

        atom, result = await self.client.http.request("DELETE", f"/guilds/{self.id}/emojis/{emoji_id}")

        if atom == 0:
            return True
        else:
            raise DeleteEmojiFailed(result)


@dataclass
class Emoji:
    """Emoji class.

    Attributes:
        id (int, None): Emoji ID.
        name (str, None): Emoji name.
        roles (list, None): Allowed roles list.
        user (User, None): Owner of the emoji.
        require_colons (bool, None): whether this emoji must be wrapped in colons.
        managed (bool, None): whether this emoji is managed.
        animated (bool, None): whether this emoji is animated.
        available (bool, None): "whether this emoji can be used, may be false due to loss of Server Boosts".
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.client = client

        self.id: Union[int, None] = int(
            data.get("id")) if data.get("id") is not None else None
        self.name: Union[str, None] = data.get("name")
        self.roles: Union[list, None] = data.get("roles")
        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.require_colons: Union[bool, None] = data.get("require_colons")
        self.managed: Union[bool, None] = data.get("managed")
        self.animated: Union[bool, None] = data.get("animated")
        self.available: Union[bool, None] = data.get("available")
