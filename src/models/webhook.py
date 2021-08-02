"""
Models for webhook and other related stuff.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class Webhook:
    """Webhook class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): Webhook ID.
        guild_id (int, None): Webhook Guild ID.
        channel_id (int, None): Webhook Channel ID.
        user (User, None): Webhook creator User object.
        name (str, None): Webhook name.
        avatar (str, None): Webhook avatar hash.
        token (str, None): Webhook secret token.
        application_id (int, None): The bot/OAuth2 application that created this webhook.
        source_guild (Guild, None): The guild of the channel that this webhook is following (returned for Channel Follower Webhooks).
        source_channel (Channel, None): The channel that this webhook is following (returned for Channel Follower Webhooks).
        url (str, None): Webhook Url.
    """

    def __init__(self, client, data: dict) -> None:
        from .guild import Guild
        from .channel import Channel
        from .user import User

        self.client = client

        self.id: int = int(data.get("id"))
        self.type: int = data.get("type")
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") is not None else None
        self.channel_id: Union[int, None] = int(
            data.get("channel_id")) if data.get("channel_id") is not None else None
        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.name: Union[str, None] = data.get("name")
        self.avatar: Union[str, None] = data.get("avatar")
        self.token: Union[str, None] = data.get("token")
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") is not None else None
        self.source_guild: Union[Guild, None] = Guild(self.client, data.get(
            "source_guild")) if data.get("source_guild") is not None else None
        self.source_channel: Union[Channel, None] = Channel(self.client, data.get(
            "source_channel")) if data.get("source_channel") is not None else None
        self.url: Union[str, None] = data.get("url")
