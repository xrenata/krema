"""
Http part of the krema.
"""

from typing import Union
import aiohttp


class HTTP:
    """Base class for HTTP.

    Args:
        client (krema.models.Client): Client class for http connection.
    """

    def __init__(self, client) -> None:
        from .models.client import Client

        self.client: Client = client
        self.url: str = "https://discord.com/api/v9"

        pass

    async def request(self, method: str, endpoint: str, params: Union[dict, list] = None) -> tuple:
        """Send a async request to the discord API.

        Args:
            method (str): REST method. like GET, PATCH etc...
            endpoint (str): Endpoint URL for request.
            params (dict): JSON Parameters for request.

        Returns:
            tuple: A tuple that contains an atom and result.
                Atom (0): Request successfully sent and got 2xx.
                Atom (1): Request failed.
        """

        if params is None:
            params = {}

        result: tuple = ()

        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.url}{endpoint}", headers={"Authorization": self.client.token, "Content-Type": "application/json", "User-Agent": "krema"}, json=params) as response:
                try:
                    json_data = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    body_text = await response.text()

                    if str(response.status).startswith("2"):
                        result = (0, "")
                    else:
                        result = (1, body_text)

                    return result

                if str(response.status).startswith("2"):
                    result = (1, json_data)
                else:
                    result = (0, json_data)

                return result
