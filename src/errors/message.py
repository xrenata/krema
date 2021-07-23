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
    """Raises when fetching the reactions are failed."""

    pass


class DeleteReactionsFailed(Exception):
    """Raises when deleting the reactions is failed."""

    pass
