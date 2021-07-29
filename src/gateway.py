"""
Gateway part of the krema.
"""

import asyncio
from json import loads
from typing import Union
from zlib import decompressobj

import aiohttp

from .models import Message, Channel, Guild


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
        self.websocket = None

        self._buffer: bytearray = bytearray()
        self._zlib = decompressobj()
        self._session: Union[aiohttp.ClientSession, None] = None

        self._seq: Union[int, None] = None
        self._session_id: Union[str, None] = None

        self._event_loop = asyncio.get_event_loop()

        self.client.events.append(
            ("ready", self.__handle_session_id)
        )

    async def __connect(self):
        """Start WebSocket connection."""

        self.websocket, self._session = None, None

        self._session = aiohttp.ClientSession()
        self.websocket = await self._session.ws_connect(self.gateway)

        # Send Resume
        if self._session_id is not None:
            # print("resume at kardes")
            await self.websocket.send_json({
                "op": 6,
                "d": {
                    "token": self.token,
                    "session_id": self._session_id,
                    "seq": self._seq
                }
            })

    async def __handle_session_id(self, packet):
        self._session_id = packet.get("session_id")

    async def __receiver(self):
        """Receive messages from WebSocket."""

        while True:
            result = await self.__handle_packet(await self.websocket.receive())

            if result is not None:
                return result

    async def __handle_packet(self, packet):
        """Handle Packets."""

        data = packet.data

        if isinstance(packet.data, int) and len(str(packet.data)) == 4:
            # Reconnect Websocket
            if packet.data == 1001:
                await self._session.close()
                self._session = None
                return 1
            else:
                print("WebSocket Exception Found: {0} ({1})".format(
                    packet.data, packet.extra))
                return 0
        elif isinstance(packet.data, type(None)):
            if packet.type == 0x101:
                return 0

        if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
            return

        # Compressor Decode
        self._buffer.extend(data)
        message = self._zlib.decompress(self._buffer).decode("utf-8")
        message = loads(message)

        self._buffer = bytearray()

        opcode, data, seq, event_type = message.get(
            "op"), message.get("d"), message.get("s"), message.get("t")

        if seq is not None:
            self._seq = seq

        # print(self._seq, self._session_id, asyncio.all_tasks(self._event_loop))
        print(message, end="\n\n")

        if opcode == self.HELLO:
            interval = data["heartbeat_interval"]
            await self.__identify(interval)

        elif opcode == self.DISPATCH:
            event_type = event_type.lower()
            if event_type in (i[0] for i in self.client.events):
                self._event_loop.create_task(
                    self.__handle_event(data, event_type))

        # Reconnect
        elif opcode == self.RECONNECT:
            return 1

    async def __handle_event(self, event_data, event_type):
        if event_type in ("message_create", "message_update"):
            if event_type == "message_update" and len(event_data) == 4:
                # print("thread galiba bu")
                return

            filtered = self.__filter_events(
                event_type, (Message(self.client, event_data),))
        elif event_type in ("guild_create", "guild_update"):
            filtered = self.__filter_events(
                event_type, (Guild(self.client, event_data),))
        elif event_type in ("channel_create", "channel_update", "channel_delete", "thread_create", "thread_update"):
            filtered = self.__filter_events(
                event_type, (Channel(self.client, event_data),))
        else:
            filtered = self.__filter_events(event_type, (event_data,))

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
            await asyncio.sleep(interval // 1000)
            if self.websocket is not None:
                await self.websocket.send_json({
                    "op": self.HEARTBEAT,
                    "d": self._seq
                })

    async def start_connection(self):
        """Start the Gateway Connection."""

        await self.__connect()
        result = await self.__receiver()

        # Reconnect
        if result == 1:
            # print("reconnect.")
            await self.start_connection()
