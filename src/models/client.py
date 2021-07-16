"""
Client model for krema.
"""


class Client:
    """Base class for client.

    Args:
        intents (int): Intents for your bot. Do not add any intent if you are using for self-bot.
        cache_limit (int): Cache limit for krema. 
    """

    def __init__(self, intents: int = 0, cache_limit: int = 200) -> None:
        self.intents: int = intents
        self.cache_limit: int = cache_limit

        self.token: str = ""
        self.events: list = []

        self.connection = None
        self.http = None

        pass

    @property
    def formatted_token(self) -> str:
        """Returns formatted version of the token.

        Returns:
            str: Formatted version of the token.
        """

        if self.token.startswith("Bot "):
            return self.token.split(" ")[1]
        else:
            return self.token

    def event(self, event_name: str = None):
        def decorator(fn):
            def wrapper():
                self.events.append(
                    (event_name or fn.__name__, fn)
                )

                return self.events

            return wrapper()

        return decorator

    def start(self, token: str, bot: bool = True):
        """Start the client.

        Args:
            token (str): Token for your bot / self-bot.
            bot (bool, optional): If you are using self-bot, make argument false.
        """

        from ..gateway import Gateway
        from ..http import HTTP

        self.token = f"Bot {token}" if bot else token

        self.connection = Gateway(self)
        self.http = HTTP(self)

        self.connection._event_loop.run_until_complete(
            self.connection.start_connection())
