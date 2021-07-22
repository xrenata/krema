"""
Errors about channels.
"""


class FetchChannelFailed(Exception):
    """Raises when fetching a channel is failed."""

    pass


class FetchChannelMessagesFailed(Exception):
    """Raises when fetching messages from channel is failed."""

    pass


class FetchChannelMessageFailed(Exception):
    """Raises when fetching A message from channel is failed."""

    pass


class BulkDeleteMessagesFailed(Exception):
    """Raises when purge messages from channel is failed."""

    pass


class EditChannelFailed(Exception):
    """Raises when editing the channel is failed."""

    pass


class DeleteChannelFailed(Exception):
    """Raises when deleting the channel is failed."""

    pass
