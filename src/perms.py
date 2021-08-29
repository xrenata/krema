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
        self.bitvise: int = int(bitvise)
        self.perms: dict = {
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

    def __str__(self) -> str:
        return str(self.list_permissions())

    def __bool__(self) -> bool:
        return self.bitvise != 0

    def __len__(self) -> int:
        return len(self.list_permissions())

    def __and__(self, item) -> int:
        return self.bitvise & item

    def __or__(self, item) -> int:
        return self.bitvise | item

    def __xor__(self, item) -> int:
        return self.bitvise ^ item

    def calculate(self, *args: str) -> int:
        """Calculate permissions and return the result.

        Args:
            *args (str): The permission name(s) will be calculated.

        Returns:
            int: Result.
        """
        result = 0

        for k, v in self.perms.items():
            if k.upper() in args:
                result = result | v

        return result

    def list_permissions(self) -> list:
        """Calculate and return list of permissions for bitvise.

        Returns:
            list: List of permissions for bitvise.
        """

        return [k for k, v in self.perms.items() if self.bitvise & v != 0]

    def has(self, permission_name: str) -> bool:
        """Check if permission includes the x.

        Args:
            permission_name (str): The permission name will be checked.

        Returns:
            bool: Result.
        """

        for k, v in self.perms.items():
            if k.upper() == permission_name:
                return self.bitvise & v != 0

        return False
