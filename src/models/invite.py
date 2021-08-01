"""
Models for invite and other related stuff.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union
from ..utils import convert_iso


@dataclass
class Invite:
    """Invite class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        guild (Guild, None): The guild this invite is for.
        channel (Channel, None): The channel this invite is for.
        inviter (User, None): Invite creator.
        target_type (int, None): The type of target for this voice channel invite.
        target_user (User, None): The user whose stream to display for this voice channel stream invite.
        target_application (dict, None): The embedded application to open for this voice channel embedded application invite.
        approximate_presence_count (int, None): Approximate count of online members.
        approximate_member_count (int, None): Approximate count of total members.
        expires_at (datetime, None): Invite expire time.
        stage_instance (dict, None): Stage instance data if there is a public Stage instance in the Stage channel this invite is for.
        uses (int, None): Number of times this invite has been used.
        max_uses (int, None): Max number of times this invite can be used.
        max_age (int, None): Duration (in seconds) after which the invite expires.
        temporary (bool, None): Whether this invite only grants temporary membership.
        created_at (datetime, None): When this invite was created.
    """

    def __init__(self, client, data: dict) -> None:
        from .guild import Guild
        from .channel import Channel
        from .user import User

        self.client = client

        self.code: str = data.get("code")
        self.guild: Union[Guild, None] = Guild(self.client, data.get(
            "guild")) if data.get("guild") is not None else None
        self.channel: Union[Channel, None] = Channel(self.client, data.get(
            "channel")) if data.get("channel") is not None else None
        self.inviter: Union[User, None] = User(self.client, data.get(
            "inviter")) if data.get("inviter") is not None else None
        self.target_type: Union[int, None] = data.get("target_type")
        self.target_user: Union[User, None] = User(self.client, data.get(
            "target_user")) if data.get("target_user") is not None else None
        self.target_application: Union[dict,
                                       None] = data.get("target_application")
        self.approximate_presence_count: Union[int, None] = data.get(
            "approximate_presence_count")
        self.approximate_member_count: Union[int, None] = data.get(
            "approximate_member_count")
        self.expires_at: Union[datetime, None] = convert_iso(
            data.get("expires_at")) if data.get("expires_at") is not None else None
        self.stage_instance: Union[dict, None] = data.get("stage_instance")
        self.uses: Union[int, None] = data.get("uses")
        self.max_uses: Union[int, None] = data.get("max_uses")
        self.max_age: Union[int, None] = data.get("max_age")
        self.temporary: Union[bool, None] = data.get("temporary")
        self.created_at: Union[datetime, None] = convert_iso(
            data.get("created_at")) if data.get("created_at") is not None else None
