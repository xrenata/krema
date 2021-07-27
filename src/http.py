"""
Http part of the krema.
"""

import asyncio
from typing import Union
import aiohttp
from .errors import *

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

    async def request(self, method: str, endpoint: str, **kwargs) -> Union[str, list, dict]:
        """Send a async request to the discord API.

        Args:
            method (str): REST method. like GET, PATCH etc...
            endpoint (str): Endpoint URL for request.
            **kwargs Other parameters for request.

        Returns:
            result (dict, list, str): Result from Discord API

        Raises:
            All of the Exceptions from `krema.errors` may raise.
        """

        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.url}{endpoint}", headers={"Authorization": self.client.token, "User-Agent": "krema"}, **kwargs) as response:
                try:
                    json_data = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    body_text = await response.text()

                    if 300 > response.status >= 200:
                        return ""
                    else:
                        self.__raise_for_status(response.status, body_text)

                if 300 > response.status >= 200:
                    return json_data
                else:
                    retry_after = json_data.get("retry_after")

                    if retry_after is not None:
                        return await self.__run_task_when_ratelimit_reset(retry_after, method, endpoint, **kwargs)
                    else:
                        self.__raise_for_status(response.status, json_data.get("message") or json_data)

    async def __run_task_when_ratelimit_reset(self, ratelimit: float, method, endpoint, **kwargs):
        await asyncio.sleep(ratelimit + 0.1)
        return await self.request(method, endpoint, **kwargs)

    def __raise_for_status(self, status: int, result: str):
        if status == 404:
            raise NotFound(result)
        elif status == 403:
            raise Forbidden(result)
        elif status == 429:
            raise RateLimited(result)
        elif 600 > status >= 500:
            raise ServerError(result)
        else:
            raise UnexceptedStatus(result)