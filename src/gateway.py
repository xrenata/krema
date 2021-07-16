"""
Gateway part of the krema.
"""

import asyncio
import aiohttp
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
        self.websocket: aiohttp._WSRequestContextManager = None

        self._buffer: bytearray = bytearray()
        self._zlib = decompressobj()
        self._session: aiohttp.ClientSession = None
        self._event_loop = asyncio.new_event_loop()

    async def __connect(self):
        """Start WebSocket connection."""

        self._session = aiohttp.ClientSession()
        self.websocket = await self._session.ws_connect(self.gateway)

    async def __receiver(self):
        """Receive messages from WebSocket."""

        while True:
            await self.__handle_packet(await self.websocket.receive())

    async def __handle_packet(self, packet):
        data = packet.data
        if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
            return

        self._buffer.extend(data)
        message = self._zlib.decompress(self._buffer).decode("utf-8")
        message = loads(message)

        self._buffer = bytearray()

        opcode, data, seq = message.get(
            "op"), message.get("d"), message.get("s")
        if opcode == self.HELLO:
            interval = data["heartbeat_interval"]
            await self.__identify(interval)
        elif opcode == self.DISPATCH:
            print(message, 1)

    async def __identify(self, interval):
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

        await self.websocket.send_json(payload)
        self._event_loop.create_task(self.__send_heartbeat(interval))

    async def __send_heartbeat(self, interval):
        while True:
            if self.websocket is not None:
                await self.websocket.send_json({
                    "op": self.HEARTBEAT,
                    "d": None
                })

                await asyncio.sleep(interval)

    async def start_connection(self):
        await self.__connect()
        await self.__receiver()
