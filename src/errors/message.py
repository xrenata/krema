"""
Errors about messages.
"""


class SendMessageFailed(Exception):
    """Raises when sending a message is failed."""

    pass


class CreateReactionFailed(Exception):
    """Raises when creating the reaction is failed."""

    pass


class DeleteReactionFailed(Exception):
    """Raises when deleting the reaction is failed."""

    pass


class FetchReactionsFailed(Exception):
    """Raises when fetching the reactions is failed."""

    pass


class DeleteReactionsFailed(Exception):
    """Raises when deleting the reactions is failed."""

    pass


class EditMessageFailed(Exception):
    """Raises when editing the message is failed."""

    pass


class DeleteMessageFailed(Exception):
    """Raises when deleting the message is failed."""

    pass


class PinMessageFailed(Exception):
    """Raises when pinning the message is failed."""

    pass


class UnpinMessageFailed(Exception):
    """Raises when unpinning the message is failed."""

    pass
