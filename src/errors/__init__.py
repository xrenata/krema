"""
All errors are collected in here.
"""

from .message import *
from .channel import *


class InvalidTokenError(Exception):
    """Raises when checking the client token failed."""

    pass
