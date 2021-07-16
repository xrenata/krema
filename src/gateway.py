"""
Gateway part of the krema.
"""

import trio
from trio_websocket import open_websocket_url
from zlib import decompressobj
from json import loads, dumps


class Gateway:
    """Base class for gateway.

    Args:
        client (krema.models.Client): Client class for gateway connection.
    """
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __init__(self, client) -> None:
        from .models.client import Client
        from typing import Coroutine

        self.client: Client = client
        self.token: str = self.client.formatted_token

        self.gateway: str = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"
        self.websocket: Coroutine = None

        self._buffer: bytearray = bytearray()
        self._zlib = decompressobj()

    async def __connect(self):
        """Start WebSocket connection."""

        async with open_websocket_url(self.gateway) as ws:
            self.websocket = ws
            await self.__receiver()

    async def __receiver(self):
        """Receive messages from WebSocket."""

        while True:
            await self.__handle_packet(await self.websocket.get_message())

    async def __handle_packet(self, packet):
        if len(packet) < 4 or packet[-4:] != b'\x00\x00\xff\xff':
            return

        self._buffer.extend(packet)
        message = self._zlib.decompress(self._buffer).decode("utf-8")
        message = loads(message)

        print(message)

        self._buffer = bytearray()

        opcode, data, seq = message.get("op"), message.get("d"), message.get("s")
        if opcode == self.HELLO:
            await self.__identify()

    async def __identify(self):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$browser": "kream",
                    "$device": "kream",
                    "$referrer": "",
                    "$referring_domain": ""
                },
                "compress": True,
                "large_threshold": 250,
                "v": 3
            }
        }

        if self.client.intents != 0:
            payload["d"]["intents"] = self.client.intents

        await self.websocket.send_message(dumps(payload))

    async def start_connection(self):
        await self.__connect()