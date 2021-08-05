"""
Models for webhook and other related stuff.
"""

from dataclasses import dataclass
from typing import Union
from ..utils import dict_to_query
from json import dumps
from aiohttp import FormData


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

    async def edit(self, **kwargs):
        """Edit Webhook.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/webhook#modify-webhook-json-params

        Returns:
            Webhook: Updated Webhook object.
        """

        result = await self.client.http.request("PATCH", f"/webhooks/{self.id}", json=kwargs)
        return Webhook(self.client, result)

    async def delete(self):
        """Delete Webhook.

        Returns:
            True: Webhook deleted successfully.
        """

        await self.client.http.request("DELETE", f"/webhooks/{self.id}")
        return True

    async def execute(self, file: dict = None, query: dict = {}, **kwargs):
        """Execute the Webhook.

        Args:
            file (dict): For send a message / embed attachment with file, use `krema.utils.file_builder` for make it easier.
            query (dict): https://discord.com/developers/docs/resources/webhook#execute-webhook-query-string-params
            **kwargs: https://discord.com/developers/docs/resources/webhook#execute-webhook-jsonform-params

        Returns:
            True: Webhook executed successfully.
        """
        params, payload = {}, FormData()

        if file is not None:
            payload.add_field(name='payload_json', value=dumps(
                kwargs), content_type="application/json")
            payload.add_field(**file)

            params["data"] = payload
        else:
            params["json"] = kwargs

        await self.client.http.request("POST", f"/webhooks/{self.id}/{self.token}{dict_to_query(query)}", **params)
        return True

    async def fetch_message(self, message_id: int):
        """Fetch Webhook Message by ID.

        Args:
            message_id (int): Webhook Message ID.

        Returns:
            Message: Found Message object.
        """

        from .message import Message

        result = await self.client.http.request("POST", f"/webhooks/{self.id}/{self.token}/messages/{message_id}")
        return Message(self.client, result)

    async def edit_message(self, message_id: int, file: dict = None, **kwargs):
        """Edit Webhook Message by ID.

        Args:
            message_id (int): Webhook Message ID.
            file (dict): For send a message / embed attachment with file, use `krema.utils.file_builder` for make it easier.
            **kwargs: https://discord.com/developers/docs/resources/webhook#edit-webhook-message-jsonform-params

        Returns:
            Message: Updated Message object.
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

        result = await self.client.http.request("PATCH", f"/webhooks/{self.id}/{self.token}/messages/{message_id}", **params)
        return Message(self.client, result)

    async def delete_message(self, message_id: int):
        """Delete Webhook Message by ID.

        Args:
            message_id (int): Webhook Message ID.

        Returns:
            True: Message deleted successfully.
        """

        await self.client.http.request("DELETE", f"/webhooks/{self.id}/{self.token}/messages/{message_id}")
        return True
