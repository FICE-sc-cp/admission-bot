from typing import Union

from app.bot.admission_api.base import BaseAPI
from app.bot.admission_api.types.register_user import RegisterUser


class UserAPI(BaseAPI):
    _path = "/users"

    async def get_user_info(self, uid: Union[str, int]):
        async with self._session.get(f'{self.path}/{uid}') as response:
            return await response.json()

    async def register_user(self, user: RegisterUser):
        async with self._session.post(f'{self.path}/',
                                      json=user.model_dump(by_alias=True, exclude_none=True)) as response:
            return await response.json()
