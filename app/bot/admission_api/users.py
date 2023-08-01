from typing import Union, Dict

from app.bot.admission_api.base import BaseAPI


class UserAPI(BaseAPI):
    _path = "/users"

    async def get_user_info(self, uid: Union[str, int]):
        async with self._session.get(f'{self.path}/{uid}') as response:
            return await response.json()

    async def set_user_details(self, uid: Union[int, str], details: Dict[str, str]):
        async with self._session.put(f'{self.path}/{uid}/registration', json=details) as response:
            return await response.json() if response.status == 400 else None

    async def register_user(self, uid: Union[int, str], username: Union[str, None], first_name: str,
                            last_name: Union[str, None]):
        json = {}
        if username is not None:
            json['username'] = username
        json['first_name'] = first_name
        if last_name is not None:
            json['last_name'] = last_name
        json['id'] = str(uid)
        async with self._session.post(f'{self.path}/', json=json) as response:
            return response.json()
