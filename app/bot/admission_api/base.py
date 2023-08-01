from typing import Optional

from aiohttp import ClientSession
from pydantic import AnyUrl
from yarl import URL

from app.settings import settings


class BaseAPI:
    _url: AnyUrl = settings.AAPI_HOST
    _path: Optional[str] = None
    _base_url: Optional[URL] = None

    def __init__(self):
        self._session = ClientSession(self.base_url, headers=self.get_headers())
        self._token = settings.AAPI_TOKEN

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self._token}'
        }

    @property
    def base_url(self) -> URL:
        if self._base_url is None:
            self._base_url = URL(f"{self._url}")

        return self._base_url

    @property
    def path(self) -> str:
        return self._base_url.path + self._path

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()
