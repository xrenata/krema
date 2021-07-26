"""
Models for guild, channel and other related stuff.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union
from json import dumps
from aiohttp import FormData

from ..errors.message import SendMessageFailed
from ..errors.channel import *


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


@dataclass
class Channel:
    """Channel class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): Channel ID.
        type (int): Channel type.
        guild_id (int, None): Guild ID.
        position (int, None): Channel position.
        permission_overwrites (list, None): List of permission_overwrite.
        name (str, None): Channel name.
        topic (str, None): Channel topic.
        nsfw (bool, None): Channel nsfw boolean.
        last_message_id (int, None): Last message ID in the channel.
        bitrate (int, None): Channel bitrate (voice).
        user_limit (int, None): "The user limit of the voice channel" (voice).
        rate_limit_per_user (int, None): Channel slowmode second.
        recipients (list, None): List of user object.
        icon (str, None): Icon hash for DM channel.
        owner_id (int, None): DM channel owner id.
        application_id (int, None): "Application id of the group DM creator if it is bot-created".
        parent_id (int, None): "for guild channels: id of the parent category for a channel (each parent category can contain up to 50 channels), for threads: id of the text channel this thread was created".
        last_pin_timestamp (datetime, None): When the last pinned message was pinned.
        rtc_region (str, None): Voice region.
        video_quality_mode (int, None): "the camera video quality mode of the voice channel, 1 when not present".
        message_count (int, None): "an approximate count of messages in a thread, stops counting at 50".
        member_count (int, None): "an approximate count of users in a thread, stops counting at 50".
        thread_metadata (dict, None): "Thread-specific fields not needed by other channels".
        member (ThreadMember, None): "Thread member object for the current user, if they have joined the thread, only included on certain API endpoints".
        default_auto_archive_duration (int, None): "Default duration for newly created threads, in minutes, to automatically archive the thread after recent activity, can be set to: 60, 1440, 4320, 10080".
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User, ThreadMember
        from ..utils import convert_iso

        self.client = client

        self.id: int = int(data.get("id"))
        self.type: int = data.get("type")
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") is not None else None
        self.position: Union[int, None] = data.get("position")
        self.permission_overwrites: Union[list, None] = data.get(
            "permission_overwrites")
        self.name: Union[str, None] = data.get("name")
        self.topic: Union[str, None] = data.get("topic")
        self.nsfw: Union[bool, None] = data.get("nsfw")
        self.last_message_id: Union[int, None] = int(
            data.get("last_message_id")) if data.get("last_message_id") is not None else None
        self.bitrate: Union[int, None] = data.get("bitrate")
        self.user_limit: Union[int, None] = data.get("user_limit")
        self.rate_limit_per_user: Union[int,
                                        None] = data.get("rate_limit_per_user")
        self.recipients: Union[list, None] = [User(self.client, i) for i in data.get(
            "recipients")] if data.get("recipients") is not None else None
        self.icon: Union[str, None] = data.get("icon")
        self.owner_id: Union[int, None] = int(
            data.get("owner_id")) if data.get("owner_id") is not None else None
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") is not None else None
        self.parent_id: Union[int, None] = int(
            data.get("parent_id")) if data.get("parent_id") is not None else None
        self.last_pin_timestamp: Union[datetime, None] = convert_iso(
            data.get("last_pin_timestamp")) if data.get("last_pin_timestamp") is not None else None
        self.rtc_region: Union[str, None] = data.get("rtc_region")
        self.video_quality_mode: Union[int,
                                       None] = data.get("video_quality_mode")
        self.message_count: Union[int, None] = data.get("message_count")
        self.member_count: Union[int, None] = data.get("member_count")
        self.thread_metadata: Union[dict, None] = data.get("thread_metadata")
        self.member: Union[ThreadMember, None] = ThreadMember(
            data.get("member")) if data.get("member") is not None else None
        self.default_auto_archive_duration: Union[int, None] = data.get(
            "default_auto_archive_duration")

        pass

    async def fetch_messages(self, limit: int = 10):
        """Fetch messages from channel.

        Args:
            limit (int): Maximum message limit (default is 10).

        Returns:
            list: List of message object.

        Raises:
            FetchChannelMessagesFailed: Fetching the messages from channel is failed.
        """
        from .message import Message

        atom, result = await self.client.http.request("GET", f"/channels/{self.id}/messages?limit={limit}")

        if atom == 0:
            return [Message(self.client, i) for i in result]
        else:
            raise FetchChannelMessagesFailed(result)

    async def purge(self, limit: int = 2):
        """Bulk-delete messages from channel.

        Args:
            limit (int): Maximum message limit (default is 2).

        Returns:
            list: List of purged? messages.

        Raises:
            BulkDeleteMessagesFailed: Channel purge is failed.
        """

        messages = await self.fetch_messages(limit)

        atom, result = await self.client.http.request("POST", f"/channels/{self.id}/messages/bulk-delete", json={
            "messages": [i.id for i in messages]
        })

        if atom == 0:
            return messages
        else:
            raise BulkDeleteMessagesFailed(result)

    async def send(self, file: dict = None, **kwargs):
        """Send message to the text-channel.

        Args:
            file (dict): For send a message / embed attachment with file, use `krema.utils.file_builder` for make it easier.
            **kwargs: https://discord.com/developers/docs/resources/channel#create-message-jsonform-params

        Returns:
            Message: Sent message object.

        Raises:
            SendMessageFailed: Sending the message is failed.
        """
        from .message import Message

        params, payload = {}, FormData()

        if file is not None:
            payload.add_field(name='payload_json', value=dumps(
                kwargs), content_type="application/json")
            payload.add_field(**file)

            params["data"] = payload
        else:
            params["json"] = kwargs

        atom, result = await self.client.http.request("POST", f"/channels/{self.id}/messages", **params)

        if atom == 0:
            return Message(self.client, result)
        else:
            raise SendMessageFailed(result)

    async def edit(self, **kwargs):
        """Edit channel with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/channel#modify-channel

        Returns:
            Channel: New channel.

        Raises:
            EditChannelFailed: Editing the channel is failed.
        """

        atom, result = await self.client.http.request("PATCH", f"/channels/{self.id}", json=kwargs)

        if atom == 0:
            return Channel(self.client, result)
        else:
            raise EditChannelFailed(result)

    async def delete(self):
        """Delete channel.

        Returns:
            Channel: Deleted channel.

        Raises:
            DeleteChannelFailed: Editing the channel is failed.
        """

        atom, result = await self.client.http.request("DELETE", f"/channels/{self.id}")

        if atom == 0:
            return Channel(self.client, result)
        else:
            raise DeleteChannelFailed(result)

    async def fetch_message(self, message_id: int):
        """Fetch a message from channel by ID.

        Args:
            message_id: Message ID.

        Returns:
            Message: Found message.

        Raises:
            FetchChannelMessageFailed: Fetching the message is failed.
        """
        from .message import Message

        atom, result = await self.client.http.request("GET", f"/channels/{self.id}/messages/{message_id}")

        if atom == 0:
            return Message(self.client, result)
        else:
            raise FetchChannelMessageFailed(result)

    async def trigger_typing(self):
        """Trigger the Channel typing.

        Returns:
            True: Typing triggered successfully.

        Raises:
            StartTypingFailed: Triggering is failed.
        """

        atom, result = await self.client.http.request("POST", f"/channels/{self.id}/typing")

        if atom == 0:
            return True
        else:
            raise StartTypingFailed(result)

    async def fetch_pinned_messages(self):
        """Fetch pinned messages from Channel.

        Returns:
            list: List of message objects.

        Raises:
            FetchPinnedMessagesFailed: Fetching the pinned messages is failed.
        """
        from .message import Message

        atom, result = await self.client.http.request("GET", f"/channels/{self.id}/pins")

        if atom == 0:
            return [Message(self.client, i) for i in result]
        else:
            raise FetchPinnedMessagesFailed(result)
