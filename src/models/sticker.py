"""
Models for sticker and other related stuffs.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class Sticker:
    """Sticker class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): Sticker ID.
        pack_id (int, None): For standard stickers, id of the pack the sticker is from.
        name (str): Sticker name.
        description (str, None): Sticker description.
        tags (str): "for guild stickers, the Discord name of a unicode emoji representing the sticker's expression. for standard stickers, a comma-separated list of related expressions."
        asset (str): Asset hash (Deprecated.)
        type (int): Sticker type.
        format_type (int): Sticker format type.
        avaible (bool, None): Whether this guild sticker can be used.
        guild_id (int, None): Guild ID.
        user (User, None): Sticker creator user object.
        sort_value (int): The standard sticker's sort order within its pack.
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.client = client

        self.id: int = int(data.get("id"))
        self.pack_id: Union[int, None] = int(
            data.get("pack_id")) if data.get("pack_id") is not None else None
        self.name: str = data.get("name")
        self.description: Union[str, None] = data.get("description")
        self.tags: str = data.get("tags")
        self.asset: str = data.get("asset")
        self.type: int = data.get("type")
        self.format_type: int = data.get("format_type")
        self.available: Union[bool, None] = data.get("available")
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") is not None else None
        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.sort_value: int = data.get("sort_value")
