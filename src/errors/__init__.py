"""
All errors are collected in here.
"""

from .message import *
from .channel import *
from .users import *
from .guild import *


class InvalidTokenError(Exception):
    """Raises when checking the client token failed."""

    pass


class ModifyClientUserFailed(Exception):
    """Raises when editing the client user is failed."""

    pass
