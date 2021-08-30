"""
Gateway part of the krema.
"""

import asyncio
from json import loads
from typing import Union
from zlib import decompressobj
import traceback
import sys

import aiohttp

from .models import Interaction, ApplicationCommand, User, Message, Channel, Guild, Role, Emoji, Sticker, Member


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
        # print(message, end="\n\n")

        if opcode == self.HELLO:
            interval = data["heartbeat_interval"]
            await self.__identify(interval)

        elif opcode == self.DISPATCH:
            event_type = event_type.lower()
            if event_type in (i[0] for i in self.client.events):
                # self._event_loop.create_task(
                #    self.__handle_event(data, event_type))
                try:
                    await self.__handle_event(data, event_type)
                except Exception as error:
                    error = getattr(error, 'original', error)
                    print("Unexcepted error while handling the event: ",
                          file=sys.stderr)
                    traceback.print_exception(
                        type(error),
                        error,
                        error.__traceback__,
                        file=sys.stderr)

        # Reconnect
        elif opcode == self.RECONNECT:
            return 1

    async def __handle_event(self, event_data, event_type):
        if event_type in ("message_create", "message_update"):
            if event_type == "message_update" and len(event_data) == 4:
                return

            filtered = self.__filter_events(
                event_type, (Message(self.client, event_data),))
        elif event_type in ("guild_create", "guild_update"):
            filtered = self.__filter_events(
                event_type, (Guild(self.client, event_data),))
        elif event_type in ("channel_create", "channel_update", "channel_delete", "thread_create", "thread_update"):
            filtered = self.__filter_events(
                event_type, (Channel(self.client, event_data),))
        elif event_type == "interaction_create":
            filtered = self.__filter_events(
                event_type, (Interaction(self.client, event_data),))
        elif event_type in ("application_command_create", "application_command_update", "application_command_delete"):
            filtered = self.__filter_events(
                event_type, (ApplicationCommand(self.client, event_data),))
        elif event_type in ("guild_ban_add", "guild_ban_remove"):
            guild_id = int(event_data.get("guild_id")) if event_data.get("guild_id") else None
            usr_obj = User(self.client, event_data.get("user")) if event_data.get("user") else None
            filtered = self.__filter_events(event_type, (guild_id, usr_obj, ))
        elif event_type in ("guild_emojis_update", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            emojis_obj = [Emoji(self.client, i) for i in event_data["emojis"]] if event_data.get("emojis") else None
            filtered = self.__filter_events(event_type, (guild_id, emojis_obj, ))
        elif event_type in ("guild_stickers_update", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            stickers_obj = [Sticker(self.client, i) for i in event_data["stickers"]] if event_data.get("stickers") else None
            filtered = self.__filter_events(event_type, (guild_id, stickers_obj, ))
        elif event_type in ("guild_integration_update", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            filtered = self.__filter_events(event_type, (guild_id, ))
        elif event_type in ("guild_member_add", "guild_member_update", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None

            del event_data["guild_id"]
            member_obj = Member(self.client, event_data)

            filtered = self.__filter_events(event_type, (guild_id, member_obj, ))
        elif event_type in ("guild_member_remove", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            usr_obj = User(self.client, event_data["user"]) if event_data.get("user") else None

            filtered = self.__filter_events(event_type, (guild_id, usr_obj, ))
        elif event_type in ("guild_role_create", "guild_role_update", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            role_obj = Role(event_data["role"]) if event_data.get("role") else None
            filtered = self.__filter_events(event_type, (guild_id, role_obj, ))
        elif event_type in ("guild_role_delete", ):
            guild_id = int(event_data["guild_id"]) if event_data.get("guild_id") else None
            role_id = int(event_data["role_id"]) if event_data.get("role_id") else None
            filtered = self.__filter_events(event_type, (guild_id, role_id, ))
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
            await self.start_connection()
