from typing import Union, Dict

from app.bot.admission_api.base import BaseAPI
from app.bot.admission_api.types.register_user import RegisterUser


class UserAPI(BaseAPI):
    _path = "/users"

    async def get_user_info(self, uid: Union[str, int]):
        async with self._session.get(f'{self.path}/{uid}') as response:
            return await response.json()

    async def set_user_details(self, uid: Union[int, str], details: Dict[str, str]):
        async with self._session.put(f'{self.path}/{uid}/registration', json=details) as response:
            return await response.json() if response.status == 400 else None

    async def register_user(self, user: RegisterUser):
        print(user.model_dump(by_alias=True, exclude_none=True))
        async with self._session.post(f'{self.path}/', json=user.model_dump(by_alias=True, exclude_none=True)) as response:
            return response.json()
