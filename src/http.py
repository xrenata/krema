"""
Http part of the krema.
"""

import asyncio
from typing import Any, Union
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

        result: tuple = ()

        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.url}{endpoint}", headers={"Authorization": self.client.token, "Content-Type": "application/json", "User-Agent": "krema"}, json=params) as response:
                try:
                    json_data = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    body_text = await response.text()

                    if response.status >= 200 and response.status < 300:
                        result = (0, "")
                    else:
                        result = (1, body_text)

                    return result

                if response.status >= 200 and response.status < 300:
                    result = (0, json_data)
                    return result
                else:
                    retry_after = json_data.get("retry_after")

                    if retry_after is not None:
                        return await self.__run_task_when_ratelimit_reset(retry_after, method, endpoint, params)
                    else:
                        result = (1, json_data.get("message") or json_data)
                        return result

    async def __run_task_when_ratelimit_reset(self, ratelimit: float, method, endpoint, params):
        await asyncio.sleep(ratelimit + 0.1)
        return await self.request(method, endpoint, params)
