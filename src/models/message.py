
"""
Models for message and other classes about message.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Attachment:
    """Attachment class.

    Args:
        data (dict): Sent packed from websocket.

    Attributes:
        id (int): Attachment ID.
        filename (str): File name.
        content_type (str, None): Content type for file.
        size (int): File size.
        url (str): Attachment URL.
        proxy_url (str): Proxy URL for attachment.
        height (int, None): Image height.
        width (int, None): Image width.
    """

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
    """Embed class.

    Args:
        data (dict): Sent packed from websocket.

    Attributes:
        title (str, None): Embed title.
        type (str, None): Embed type like rich etc...
        description (str, None): Embed description.
        url (str, None): Embed URL.
        timestamp (datetime, None): Embed timestamp.
        color (int, None): Embed color in integer, for hex value use hex() function.
        footer (dict, None): Embed footer object.
        image (dict, None): Embed image object.
        thumbnail (dict, None): Embed thumbnail object.
        video (dict, None): Embed video object.
        provider (dict, None): Embed provider object.
        author (dict, None): Embed author object.
        fields (list, None): List of embed field.
    """

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
    """Message class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packed from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): Message ID.
        channel_id (int): Channel ID.
        guild_id (int, None): Guild ID.
        author (User, int, None): Message author.
        member (Member, int, None): Message author member object.
        content (str): Message content.
        timestamp (datetime): Message timestamp.
        edited_timestamp (datetime, None): Message edit timestamp.
        tts (bool): Message tts boolean value.
        mention_everyone (bool): Message has a everyone mention.
        mentions (list): List of mentions in message.
        mention_roles (list): List of role mentions in message.
        mention_channels (list, None): List of channel mentions in message.
        attachments (list): List of attachment object in message.
        embeds (list): List of embed object in message.
        reactions (list, None): List of reaction object in message.
        nonce (int, str, None): "Used for validating a message was sent".
        pinned (bool): Is message pinned.
        webhook_id (int, None): Webhook ID if the message sent by a webhook.
        type (int): Message type.
        activity (dict, None): Activity in the message object.
        application (dict, None): Application in the message object.
        application_id (int, None): "If the message is a response to an Interaction, this is the id of the interaction's application".
        message_reference (dict, None): Message reference object for reply, crosspost etc...
        flags (int, None): Message flags.
        interaction (dict, None): "Sent if the message is a response to an interaction".
        thread (dict, None): "the thread that was started from this message, includes thread member object".
        components (list, None): List of message components.
        sticker_items (list, None): List of message sticker item object.
        stickers (list, None): List of message sticker object (Deprecated).
    """

    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        from .user import User, Member
        from .guild import Channel

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
        self.mention_roles: list = data.get("mention_roles")
        self.mention_channels: Union[list, None] = data.get("mention_channels")

        self.attachments: list = [Attachment(i)
                                  for i in data.get("attachments")]
        self.embeds: list = [Embed(i) for i in data.get("embeds")]
        self.reactions: Union[list, None] = data.get("reactions")
        self.nonce: Union[int, str, None] = data.get("nonce")
        self.pinned: bool = data.get("pinned")
        self.webhook_id: Union[int, None] = int(
            data.get("webhook_id")) if data.get("webhook_id") else None
        self.type: int = data.get("type")
        self.activity: Union[dict, None] = data.get("activity")
        self.application: Union[dict, None] = data.get("application")
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") else None
        self.message_reference: Union[dict,
                                      None] = data.get("message_reference")
        self.flags: Union[int, None] = data.get("flags")
        self.interaction: Union[dict, None] = data.get("interaction")

        self.thread: Union[Channel, None] = Channel(
            data.get("thread")) if data.get("thread") else None

        self.components: Union[list, None] = data.get("components")
        self.sticker_items: Union[list, None] = data.get("sticker_items")
        self.stickers: Union[list, None] = data.get("stickers")