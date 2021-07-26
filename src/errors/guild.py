"""
Errors about guild.
"""


class FetchEmojisFailed(Exception):
    """Raises when fetching the list of emojis from guild is failed."""

    pass


class FetchEmojiFailed(Exception):
    """Raises when fetching the emoji from guild is failed."""

    pass


class CreateEmojiFailed(Exception):
    """Raises when creating the guild emoji is failed."""

    pass


class UpdateEmojiFailed(Exception):
    """Raises when updating the guild emoji is failed."""

    pass


class DeleteEmojiFailed(Exception):
    """Raises when deleting the guild emoji is failed."""

    pass
