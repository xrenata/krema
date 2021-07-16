from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class User:
    def __init__(self, client, data: dict) -> None:
        self.client = client

        self.id: int = int(data.get("id"))
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: Union[str, None] = data.get("avatar")
        self.bot: bool = data.get("bot") or False
        self.system: Union[bool, None] = data.get("system")
        self.mfa_enabled: Union[bool, None] = data.get("mfa_enabled")
        self.locale: Union[str, None] = data.get("locale")
        self.verified: Union[bool, None] = data.get("verified")
        self.email: Union[str, None] = data.get("email")
        self.flags: Union[int, None] = data.get("flags")
        self.premium_type: Union[int, None] = data.get("premium_type")
        self.public_flags: Union[int, None] = data.get("public_flags")


@dataclass
class Member:
    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        self.client = client

        self.user: Union[User, None] = data.get("user")
        self.nick: Union[str, None] = data.get("nick")
        self.roles: list = data.get("roles")
        self.pending: Union[bool, None] = data.get("pending")
        self.permissions: Union[str, None] = data.get("permissions")
        self.joined_at: Union[str, datetime, None] = convert_iso(
            data.get("joined_at")) if data.get("joined_at") else None
        self.premium_since: Union[str, datetime, None] = convert_iso(
            data.get("premium_since")) if data.get("premium_since") else None
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
