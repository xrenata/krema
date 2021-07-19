"""
Gateway part of the krema.
"""

import asyncio
import aiohttp
from zlib import decompressobj
from json import loads


class Gateway:
    """Base class for gateway.

    Args:
        client (krema.models.Client): Client class for gateway connection.
    """

    DISPATCH: int = 0
    HEARTBEAT: int = 1
    IDENTIFY: int = 2
    PRESENCE: int = 3
    VOICE_STATE: int = 4
    VOICE_PING: int = 5
    RESUME: int = 6
    RECONNECT: int = 7
    REQUEST_MEMBERS: int = 8
    INVALID_SESSION: int = 9
    HELLO: int = 10
    HEARTBEAT_ACK: int = 11
    GUILD_SYNC: int = 12

    def __init__(self, client) -> None:
        from .models.client import Client

        self.client: Client = client
        self.token: str = self.client.formatted_token

        self.gateway: str = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"
        self.websocket: aiohttp._WSRequestContextManager = None

        self._buffer: bytearray = bytearray()
        self._zlib = decompressobj()
        self._session: aiohttp.ClientSession = None

        self._event_loop = asyncio.get_event_loop()

    async def __connect(self):
        """Start WebSocket connection."""

        self._session = aiohttp.ClientSession()
        self.websocket = await self._session.ws_connect(self.gateway)

    async def __receiver(self):
        """Receive messages from WebSocket."""

        while True:
            await self.__handle_packet(await self.websocket.receive())

    async def __handle_packet(self, packet):
        """Handle Packets."""

        data = packet.data

        if isinstance(packet.data, int) and len(str(packet.data)) == 4:
            # Reconnect Websocket
            if packet.data == 1001:
                self._session.close()
                self._session = None
                return 1
            else:
                print("WebSocket Exception Found: {0} ({1})".format(
                    packet.data, packet.extra))
                return 0
        elif isinstance(packet.data, type(None)):
            if packet.type == 0x101:
                return 0x0

        if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
            return

        self._buffer.extend(data)
        message = self._zlib.decompress(self._buffer).decode("utf-8")
        message = loads(message)

        self._buffer = bytearray()

        opcode, data, seq, event_type = message.get(
            "op"), message.get("d"), message.get("s"), message.get("t")

        if opcode == self.HELLO:
            interval = data["heartbeat_interval"]
            await self.__identify(interval)

        elif opcode == self.DISPATCH:
            event_type = event_type.lower()
            if event_type in (i[0] for i in self.client.events):
                self._event_loop.create_task(
                    self.__handle_event(data, event_type))

            # print(message, end="\n\n")

    async def __handle_event(self, event_data, event_type):
        from .models.message import Message

        if event_type in ("message_create", "message_update"):
            filtered = self.__filter_events(
                event_type, (Message(self.client, event_data), ))
        else:
            filtered = self.__filter_events(event_type, (event_data, ))

        await asyncio.gather(*filtered)

    def __filter_events(self, event_type, args):
        return [
            i[1](*args) for i in self.client.events if i[0] == event_type
        ]

    async def __identify(self, interval):
        """Identify the Bot."""

        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$browser": "krema",
                    "$device": "krema",
                    "$referrer": "",
                    "$referring_domain": ""
                },
                "compress": True,
                "large_threshold": 250
            }
        }

        if self.client.intents != 0:
            payload["d"]["intents"] = self.client.intents

        await self.websocket.send_json(payload)
        asyncio.run_coroutine_threadsafe(
            self.__send_heartbeat(interval), self._event_loop)

    async def __send_heartbeat(self, interval):
        """Send hearbeat to the WebSocket."""

        while True:
            if self.websocket is not None:
                await self.websocket.send_json({
                    "op": self.HEARTBEAT,
                    "d": None
                })

                await asyncio.sleep(interval // 1000)

    async def start_connection(self):
        """Start the Gateway Connection."""

        await self.__connect()
        result = await self.__receiver()

        # Reconnect Websocket
        if result == 1:
            self.start_connection()
