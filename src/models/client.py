"""
Client model for krema.
"""

from typing import Union

from unikorn import kollektor
from ..utils import image_to_data_uri


class Client:
    """Base class for client.

    Args:
        intents (int): Intents for your bot. Do not add any intent if you are using for self-bot.
        message_limit (int): Message cache limit for krema (default is 200). 
        channel_limit (int): Channel cache limit for krema (default is None). 
        guild_limit (int): Guild cache limit for krema (default is None). 

    Attributes:
        token (str): Bot token for http request.
        events (list): List of events for client.
        user (User): Client user.
        messages (kollektor.Kollektor): Message cache.
        guilds (kollektor.Kollektor): Guild cache.
        channels (kollektor.Kollektor): Channel cache.
        connection (Gateway): Client gateway.
        connection (HTTP): Client http class.
    """

    def __init__(self, intents: int = 0, message_limit: int = 200, channel_limit: int = None,
                 guild_limit: int = None) -> None:
        from .user import User

        self.intents: int = intents

        self.token: str = ""
        self.events: list = []
        self.user: Union[User, None] = None

        self.messages: kollektor.Kollektor = kollektor.Kollektor(
            limit=message_limit, items=())
        self.guilds: kollektor.Kollektor = kollektor.Kollektor(
            limit=guild_limit, items=())
        self.channels: kollektor.Kollektor = kollektor.Kollektor(
            limit=channel_limit, items=())

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

    async def check_token(self):
        """Check token status for client.

        Returns:
            None: Client token works.
        """

        from .user import User
        result = await self.http.request("GET", "/users/@me")
        self.user = User(self, result)

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

        self.connection._event_loop.run_until_complete(self.check_token())
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
                self.messages.items = tuple(
                    i for i in self.messages.items if i.id != message_id)

        # Message Bulk Delete Handler
        async def _message_delete_bulk(packet):
            message_ids = packet.get("ids")

            if message_ids is None:
                return
            else:
                message_ids = tuple(int(i) for i in message_ids)
                self.messages.items = tuple(
                    i for i in self.messages.items if i.id not in message_ids)

        # Guild Create Handler
        async def _guild_create(guild):
            self.guilds.append(guild)

            # Add Guild Channels
            if guild.channels is not None:
                self.channels.append(*guild.channels)

        # Guild Update Handler
        async def _guild_update(guild_packet):
            for index, guild in enumerate(self.guilds.items):
                if guild.id == guild_packet.id:
                    self.guilds.update(index, guild_packet)
                    break

        # Guild Delete Handler
        async def _guild_delete(packet):
            guild_id = packet.get("id")

            if guild_id is None:
                return
            else:
                guild_id = int(guild_id)
                self.guilds.items = tuple(
                    i for i in self.guilds.items if i.id != guild_id)

        # Channel Create Handler
        async def _channel_create(channel):
            self.channels.append(channel)

        # Channel Update Handler
        async def _channel_update(channel_packet):
            for index, channel in enumerate(self.channels.items):
                if channel.id == channel_packet.id:
                    self.channels.update(index, channel_packet)
                    break

        # Channel Delete Handler
        async def _channel_delete(channel_packet):
            channel_id = hasattr(channel_packet, "id")

            if channel_id is None:
                return
            else:
                self.channels.items = tuple(
                    i for i in self.channels.items if i.id != channel_packet.id)

        # Thread Create Handler
        async def _thread_create(channel):
            self.channels.append(channel)

        # Thread Update Handler
        async def _thread_update(channel_packet):
            for index, channel in enumerate(self.channels.items):
                if channel.id == channel_packet.id:
                    self.channels.update(index, channel_packet)
                    break

        # Thread Delete Handler
        async def _thread_delete(channel_packet):
            channel_id = channel_packet.get("id")

            if channel_id is None:
                return
            else:
                channel_id = int(channel_id)
                self.channels.items = tuple(
                    i for i in self.channels.items if i.id != channel_id)

        local = locals()

        # Load Events
        self.events.extend(
            (i[1:], local[i]) for i in local if i.startswith("_")
        )

    # Cache Functions
    # ==================

    def get_guild(self, guild_id: int):
        """Get Guild from Cache by ID.

        Args:
            guild_id (int): Guild ID.

        Returns:
            Guild: Found Guild object.
            None: Guild is not Found.
        """

        result = self.guilds.find(lambda g: g.id == guild_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_channel(self, channel_id: int):
        """Get Channel from Cache by ID.

        Args:
            channel_id (int): Channel ID.

        Returns:
            Channel: Found Channel object.
            None: Channel is not Found.
        """

        result = self.channels.find(lambda c: c.id == channel_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_message(self, message_id: int):
        """Get Message from Cache by ID.

        Args:
            message_id (int): Message ID.

        Returns:
            Message: Found Message object.
            None: Message is not Found.
        """

        result = self.messages.find(lambda m: m.id == message_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_thread(self, thread_id: int, list_thread_result: dict):
        """Get Thread-Channel with Thread ID.

        Args:
            thread_id (int): Thread-Channel ID.
            list_thread_result (dict): The result from `<Channel>.list_...` functions.

        Returns:
            Channel: Found Thread-Channel object.
            None: Thread-Channel is not Found.

        Examples:
            >>> channel = client.get_channel(123)
            >>> thread_list = await channel.list_threads()
            >>> client.get_thread(456, thread_list)
            Channel()
        """

        for thread in list_thread_result["threads"]:
            if thread_id == thread.id:
                return thread

        return None

    # Gateway Functions
    # ==================

    async def update_presence(self, packet: dict):
        """Update client-user presence.

        Args:
            packet (dict): https://discord.com/developers/docs/topics/gateway#update-presence-gateway-presence-update-structure
        """

        await self.connection.websocket.send_json({
            "op": 3,
            "d": packet
        })

    # Endpoint Functions
    # ==================

    async def fetch_channel(self, id: int):
        """Fetch a Channel by ID.

        Args:
            id (int): Channel ID.

        Returns:
            Channel: Found channel.
        """

        from .channel import Channel

        result = await self.http.request("GET", f"/channels/{id}")
        return Channel(self, result)

    async def fetch_user(self, id: int = None):
        """Fetch an User by ID.

        Args:
            id (int, optional): User ID, if not added it will fetch client user (@me).

        Returns:
            User: Found user.
        """

        from .user import User

        result = await self.http.request("GET", f"/users/{id if id is not None else '@me'}")
        return User(self, result)

    async def create_guild(self, **kwargs):
        """Create a Guild with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#create-guild-json-params.

        Returns:
            Guild: Created guild object.
        """

        from .guild import Guild

        result = await self.http.request("POST", f"/guilds", json=kwargs)
        return Guild(self, result)

    async def fetch_guild(self, guild_id: int, with_count: bool = False):
        """Fetch a Guild by ID.

        Args:
            guild_id (int): Guild ID.
            with_count (bool, optional): if True, will return approximate member and presence counts for the guild. (default False)

        Returns:
            Guild: Found guild object.
        """

        from .guild import Guild

        result = await self.http.request("GET", f"/guilds/{guild_id}?with_count={with_count}")
        return Guild(self, result)

    async def edit(self, username: str, path: str):
        """Edit client user.

        Args:
            username (str): New username.
            path (str): Image / Gif path.

        Returns:
            User: Updated user.
        """

        from .user import User

        result = await self.http.request("PATCH", "/users/@me", json={
            "username": username,
            "avatar": image_to_data_uri(path)
        })
        return User(self, result)

    async def edit_nickname(self, guild_id: int, nick: str):
        """Edit Client User nickname from Guild.

        Args:
            guild_id (int): Guild ID.
            nick (str): New nickname for Client User.

        Returns:
            True: Nickname updated successfully.
        """

        await self.http.request("PATCH", f"/guilds/{guild_id}/members/@me/nick", json={
            "nick": nick
        })
        return True
