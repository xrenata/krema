"""
Client model for krema.
"""

from unikorn import kollektor
from ..errors import *


class Client:
    """Base class for client.

    Args:
        intents (int): Intents for your bot. Do not add any intent if you are using for self-bot.
        cache_limit (int): Cache limit for krema. 
    """

    def __init__(self, intents: int = 0, cache_limit: int = 200) -> None:
        self.intents: int = intents
        self.cache_limit: int = cache_limit

        self.token: str = ""
        self.events: list = []

        self.messages: kollektor.Kollektor = kollektor.Kollektor()

        self.connection = None
        self.http = None

        self.__add_cache_events()

        pass

    @property
    def formatted_token(self) -> str:
        """Returns formatted version of the token.

        Returns:
            str: Formatted version of the token.
        """

        if self.token.startswith("Bot "):
            return self.token.split(" ")[1]
        else:
            return self.token

    def event(self, event_name: str = None):
        """Event decorator for handle gateway events.

        Args:
            event_name (str, optional): Event name in lowercase. Example MESSAGE_CREATE is message_create for krema. If you don't add this argument, It will get the name from function name.

        """

        def decorator(fn):
            def wrapper():
                self.events.append(
                    (event_name or fn.__name__, fn)
                )

                return self.events

            return wrapper()

        return decorator

    def start(self, token: str, bot: bool = True):
        """Start the client.

        Args:
            token (str): Token for your bot / self-bot.
            bot (bool, optional): If you are using self-bot, make argument false.
        """

        from ..gateway import Gateway
        from ..http import HTTP

        self.token = f"Bot {token}" if bot else token

        self.connection = Gateway(self)
        self.http = HTTP(self)

        self.connection._event_loop.run_until_complete(
            self.connection.start_connection())

    # Handler for Cache Events.
    def __add_cache_events(self):
        # Message Add Handler
        async def _message_create(message_packet):
            self.messages.append(message_packet)

        # Message Update Handler
        async def _message_update(message_packet):
            for index, message in enumerate(self.messages.items):
                if message.id == message_packet.id:
                    self.messages.update(index, message_packet)
                    break

        # Message Delete Handler
        async def _message_delete(packet):
            message_id = packet.get("id")

            if message_id is None:
                return
            else:
                message_id = int(message_id)

                for message in self.messages.items:
                    if message.id == message_id:
                        self.messages.items = tuple(
                            i for i in self.messages.items if i.id != message.id)
                        break

        event_list: dict = {
            "message_create": _message_create,
            "message_update": _message_update,
            "message_delete": _message_delete
        }

        # Load Events
        self.events.extend(
            (key, value) for key, value in event_list.items()
        )

    # Endpoint Functions
    # ==================

    async def send_message(self, id: int, **kwargs):
        """Send message to the text-channel.

        Args:
            id (int): Channel ID.
            **kwargs: https://discord.com/developers/docs/resources/channel#create-message-jsonform-params

        Returns:
            Message: Sent message object.

        Raises:
            SendMessageFailed: Sending the message is failed.
        """

        from .message import Message

        atom, result = await self.http.request("POST", f"/channels/{id}/messages", kwargs)

        print(kwargs, id)

        if atom == 0:
            return Message(self, result)
        else:
            raise SendMessageFailed(result)
