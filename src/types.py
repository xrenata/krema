"""
Krema part for Perms, Types, Intents etc...
"""


class ChannelTypes:
    """All Channel types in this class."""

    GUILD_TEXT: int = 0  # a text channel within a server
    DM: int = 1  # a direct message between users
    GUILD_VOICE: int = 2  # a voice channel within a server
    GROUP_DM: int = 3  # a direct message between multiple users
    GUILD_CATEGORY: int = 4  # an organizational category that contains up to 50 channels
    GUILD_NEWS: int = 5  # a channel that users can follow and crosspost into their own server
    GUILD_STORE: int = 6  # a channel in which game developers can sell their game on Discord
    GUILD_NEWS_THREAD: int = 10  # a temporary sub-channel within a GUILD_NEWS channel
    GUILD_PUBLIC_THREAD: int = 11  # a temporary sub-channel within a GUILD_TEXT channel
    # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
    GUILD_PRIVATE_THREAD: int = 12
    GUILD_STAGE_VOICE: int = 13  # a voice channel for hosting events with an audience


class Intents:
    """Intent constants."""

    GUILDS: int = 1 << 0
    GUILD_MEMBERS: int = 1 << 1
    GUILD_BANS: int = 1 << 2
    GUILD_EMOJIS_AND_STICKERS: int = 1 << 3
    GUILD_INTEGRATIONS: int = 1 << 4
    GUILD_WEBHOOKS: int = 1 << 5
    GUILD_INVITES: int = 1 << 6
    GUILD_VOICE_STATES: int = 1 << 7
    GUILD_PRESENCES: int = 1 << 8
    GUILD_MESSAGES: int = 1 << 9
    GUILD_MESSAGE_REACTIONS: int = 1 << 10
    GUILD_MESSAGE_TYPING: int = 1 << 11
    DIRECT_MESSAGES: int = 1 << 12
    DIRECT_MESSAGE_REACTIONS: int = 1 << 13
    DIRECT_MESSAGE_TYPING: int = 1 << 14

    def All(self):
        attrs = [i for i in dir(self) if not i.startswith("__") and i != "All"]
        result = sum(int(getattr(self, i)) for i in attrs)

        return result
