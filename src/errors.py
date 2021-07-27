"""
Error classes for HTTP Exceptions.
"""


class NotFound(Exception):
    """Raises when Discord returns 404 (not found)."""

    pass


class Forbidden(Exception):
    """Raises when Discord returns 403 (forbidden)."""

    pass


class ServerError(Exception):
    """Raises when Discord returns 500 >= (internal server error)."""

    pass


class RateLimited(Exception):
    """Raises when Discord returns 429 (rate-limited)."""

    pass


class UnexceptedStatus(Exception):
    """Raises when Discord returns other statuses."""

    pass
