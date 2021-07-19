"""
Errors about channels.
"""


class FetchChannelFailed(Exception):
    """Raises when fetching a channel is failed."""

    pass


class FetchChannelMessagesFailed(Exception):
    """Raises when fetching messages from channel is failed."""

    pass
