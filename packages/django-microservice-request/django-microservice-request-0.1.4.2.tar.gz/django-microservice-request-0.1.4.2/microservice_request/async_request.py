import asyncio
import httpx
from typing import Union, List
from django.conf import settings


class AsyncRequest:
    service: str = None
    url: str = ''
    api_header = getattr(settings, 'API_KEY_HEADER', 'X-ACCESS-KEY')
    api_key: str = ''

    def __init__(self, request, url: str = None):
        self.loop = asyncio.get_event_loop()
        self.request = request
        self.url = url

    @property
    async def authorization_header(self) -> dict:
        return {"Authorization": f"{self.api_header} {self.api_key}"}

    @property
    async def headers(self) -> dict:
        headers = await self.authorization_header
        return headers

    async def post(self, data: Union[dict, List[dict]] = None, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.post(url=self.url, data=data, headers=self.headers)
