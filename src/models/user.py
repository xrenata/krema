"""
Models for user and other classes about user.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class User:
    """User class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): User ID.
        username (str): Username of the user.
        discriminator (str): User discriminator (like 0001, 1337.).
        avatar (str, None): Avatar hash for user.
        bot (bool): True if user is a bot, False if is not.
        system (bool, None): "Whether the user is an Official Discord System user".
        mfa_enabled (bool, None): "Whether the user has two factor enabled on their account".
        locale (str, None): "the user's chosen language option".
        verified (bool, None): "Whether the email on this account has been verified".
        email (str, None): User email.
        flags (int, None): the flags on the user account.
        premium_type (int, None): "the type of Nitro subscription on a user's account".
        flags (int, None): The public flags on the user account.
        flags_dict (dict): Flags dictionary for calculating.
    """

    def __init__(self, client, data: dict) -> None:
        self.client = client

        self.id: int = int(data.get("id"))
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: Union[str, None] = data.get("avatar")
        self.banner: Union[str, None] = data.get("banner")
        self.banner_color: Union[str, None] = data.get("banner_color")
        self.accent_color: Union[int, None] = data.get("accent_color")
        self.bot: bool = data.get("bot", False)
        self.system: Union[bool, None] = data.get("system")
        self.mfa_enabled: Union[bool, None] = data.get("mfa_enabled")
        self.locale: Union[str, None] = data.get("locale")
        self.verified: Union[bool, None] = data.get("verified")
        self.email: Union[str, None] = data.get("email")
        self.flags: Union[int, None] = data.get("flags")
        self.premium_type: Union[int, None] = data.get("premium_type")
        self.public_flags: Union[int, None] = data.get("public_flags")

        self.flags_dict: dict = {
            "DISCORD_EMPLOYEE": 1 << 0,
            "PARTNERED_SERVER_OWNER": 1 << 1,
            "HYPESQUAD_EVENTS": 1 << 2,
            "BUG_HUNTER_LEVEL_1": 1 << 3,
            "HOUSE_BRAVERY": 1 << 6,
            "HOUSE_BRILLIANCE": 1 << 7,
            "HOUSE_BALANCE": 1 << 8,
            "EARLY_SUPPORTER": 1 << 9,
            "TEAM_USER": 1 << 10,
            "BUG_HUNTER_LEVEL_2": 1 << 14,
            "VERIFIED_BOT": 1 << 16,
            "EARLY_VERIFIED_BOT_DEVELOPER": 1 << 17,
            "DISCORD_CERTIFIED_MODERATOR": 1 << 18
        }

    def has_public_flag(self, flag_name: str) -> bool:
        """Check if user has a public flag named x.

        Args:
            flag_name: The flag name will be checked.

        Returns:
            bool: Result
        """

        if self.public_flags is None:
            return False

        for k, v in self.flags_dict.items():
            if k.upper() == flag_name:
                return self.public_flags & v != 0

        return False

    def list_public_flags(self) -> list:
        """List flags for the user.

        Returns:
            list: Found public flags.
        """

        if self.public_flags is None:
            return []

        return [k for k, v in self.flags_dict.items() if self.public_flags & v != 0]


@dataclass
class Member:
    """Member class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        user (User, None): User object for member.
        nick (str, None): Member nickname in the guild.
        roles (list, None): List of role IDs.
        pending (bool, None): "Whether the user has not yet passed the guild's Membership Screening requirements".
        permissions (str, None): "Total permissions of the member in the channel, including overwrites, returned when in the interaction object".
        joined_at (datetime, None): When the member joined to the guild.
        premium_since (datetime, None): When the user boosted the guild.
        deaf (bool): "Whether the user is deafened in voice channels".
        mute (bool): "Whether the user is muted in voice channels".
    """

    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        self.client = client

        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.nick: Union[str, None] = data.get("nick")
        self.roles: list = data.get("roles")
        self.pending: Union[bool, None] = data.get("pending")
        self.permissions: Union[str, None] = data.get("permissions")
        self.joined_at: Union[datetime, None] = convert_iso(
            data.get("joined_at")) if data.get("joined_at") is not None else None
        self.premium_since: Union[datetime, None] = convert_iso(
            data.get("premium_since")) if data.get("premium_since") is not None else None
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")


@dataclass
class ThreadMember:
    """Thread-member class.

    Args:
        data (dict): Sent packet from websocket.

    Attributes:
        id (int, None): The ID of the thread.
        user_id (int, None): The ID of the user.
        join_timestamp (datetime, None): "The time the current user last joined the thread".
        flags (int): "Any user-thread settings, currently only used for notifications".
    """

    def __init__(self, data: dict) -> None:
        from ..utils import convert_iso

        self.id: Union[int, None] = int(
            data.get("id")) if data.get("id") is not None else None
        self.user_id: Union[int, None] = int(
            data.get("user_id")) if data.get("user_id") is not None else None
        self.join_timestamp: Union[int, None] = convert_iso(
            data.get("join_timestamp")) if data.get("join_timestamp") is not None else None
        self.flags: int = data.get("flags")
