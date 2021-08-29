"""
Permission utils for Krema.
"""
from typing import Union


class Permissions:
    """Permissions class.

    Args:
        bitvise (str, int): The bitvise permission.

    Attributes:
        bitvise (int): Bitvise permission.
        perms (dict): Permissions dictionary.
    """
    
    def __init__(self, bitvise: Union[str, int]) -> None:
        self.bitvise = int(bitvise)
        self.perms = {
            "CREATE_INSTANT_INVITE": 1 << 0,
            "KICK_MEMBERS": 1 << 1,
            "BAN_MEMBERS": 1 << 2,
            "ADMINISTRATOR": 1 << 3,
            "MANAGE_CHANNELS": 1 << 4,
            "MANAGE_GUILD": 1 << 5,
            "ADD_REACTIONS": 1 << 6,
            "VIEW_AUDIT_LOG": 1 << 7,
            "PRIORITY_SPEAKER": 1 << 8,
            "STREAM": 1 << 9,
            "VIEW_CHANNEL": 1 << 10,
            "SEND_MESSAGES": 1 << 11,
            "SEND_TTS_MESSAGES": 1 << 12,
            "MANAGE_MESSAGES": 1 << 13,
            "EMBED_LINKS": 1 << 14,
            "ATTACH_FILES": 1 << 15,
            "READ_MESSAGE_HISTORY": 1 << 16,
            "MENTION_EVERYONE": 1 << 17,
            "USE_EXTERNAL_EMOJIS": 1 << 18,
            "VIEW_GUILD_INSIGHTS": 1 << 19,
            "CONNECT": 1 << 20,
            "SPEAK": 1 << 21,
            "MUTE_MEMBERS": 1 << 22,
            "DEAFEN_MEMBERS": 1 << 23,
            "MOVE_MEMBERS": 1 << 24,
            "USE_VAD": 1 << 25,
            "CHANGE_NICKNAME": 1 << 26,
            "MANAGE_NICKNAMES": 1 << 27,
            "MANAGE_ROLES": 1 << 28,
            "MANAGE_WEBHOOKS": 1 << 29,
            "MANAGE_EMOJIS_AND_STICKERS": 1 << 30,
            "USE_APPLICATION_COMMANDS": 1 << 31,
            "REQUEST_TO_SPEAK": 1 << 32,
            "MANAGE_THREADS": 1 << 34,
            "USE_PUBLIC_THREADS": 1 << 35,
            "USE_PRIVATE_THREADS": 1 << 36,
            "USE_EXTERNAL_STICKERS": 1 << 37
        }
