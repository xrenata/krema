from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Attachment:
    def __init__(self, data: dict) -> None:
        self.id: int = int(data.get("id"))
        self.filename: str = data.get("filename")
        self.content_type: Union[str, None] = data.get("content_type")
        self.size: int = data.get("size")
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")

        self.height: Union[int, None] = data.get("height")
        self.width: Union[int, None] = data.get("width")


@dataclass
class Embed:
    def __init__(self, data: dict) -> None:
        from ..utils import convert_iso

        self.title: Union[str, None] = data.get("title")
        self.type: Union[str, None] = data.get("type")
        self.description: Union[str, None] = data.get("description")
        self.url: Union[str, None] = data.get("url")
        self.timestamp: Union[datetime, None] = convert_iso(
            data.get("timestamp")) if data.get("timestamp") else None
        self.color: Union[int, None] = data.get("color")
        self.footer: Union[dict, None] = data.get("footer")
        self.image: Union[dict, None] = data.get("image")
        self.thumbnail: Union[dict, None] = data.get("thumbnail")
        self.video: Union[dict, None] = data.get("video")
        self.provider: Union[dict, None] = data.get("provider")
        self.author: Union[dict, None] = data.get("author")
        self.fields: Union[list, None] = data.get("fields")


@dataclass
class Message:
    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        from .user import User, Member

        self.client = client

        self.id: int = int(data.get("id"))
        self.channel_id: int = int(data.get("channel_id"))
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") else None
        self.author: Union[User, int, None] = User(
            self.client, data.get("author")) if data.get("author") else None
        self.member: Union[Member, int, None] = Member(
            self.client, data.get("author")) if data.get("author") else None
        self.content: str = data.get("content")
        self.timestamp: datetime = convert_iso(data.get("timestamp"))
        self.edited_timestamp: Union[datetime, None] = convert_iso(
            data.get("edited_timestamp")) if data.get("edited_timestamp") else None
        self.tts: bool = data.get("tts")
        self.mention_everyone: bool = data.get("mention_everyone")

        self.mentions: list = data.get("mentions")
        self.mention_channels: list = data.get("mention_channels")
        self.mention_channels: list = data.get("mention_channels")

        self.attachments: list = [Attachment(i)
                                  for i in data.get("attachments")]
        self.embeds: list = [Embed(i) for i in data.get("embeds")]
        self.reactions: Union[list, None] = data.get("reactions")
        self.nonce: Union[int, str, None] = data.get("nonce")
        self.pinned: bool = data.get("pinned")
        self.webhook_id: Union[int, None] = int(data.get("webhook_id")) if data.get("webhook_id") else None
        self.type: int = data.get("type")
        self.activity: Union[dict, None] = data.get("activity")
        self.application: Union[dict, None] = data.get("application")
        self.application_id: Union[int, None] = int(data.get("application_id")) if data.get("application_id") else None
        self.message_reference: Union[dict, None] = data.get("message_reference")
        self.flags: Union[int, None] = data.get("flags")
        self.interaction: Union[dict, None] = data.get("interaction")
        self.thread: Union[dict, None] = data.get("thread")
