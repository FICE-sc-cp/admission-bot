from typing import Union

from app.bot.admission_api.base import BaseAPI


class QueueAPI(BaseAPI):
    _path = "/queues"

    async def add_user_to_queue(self, queue_id: Union[str, int], uid: Union[str, int]):
        async with self._session.post(f"{self.path}/{queue_id}/users", json={"id": str(uid)}) as response:
            return await response.json(content_type=None)

    async def remove_user_from_queue(self, queue_id: Union[str, int], uid: Union[str, int]):
        async with self._session.delete(f'{self.path}/{queue_id}/users/{uid}') as response:
            return await response.json(content_type=None)

    async def list_queues(self):
        async with self._session.get(f'{self.path}/') as response:
            return await response.json(content_type=None)
