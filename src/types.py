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
