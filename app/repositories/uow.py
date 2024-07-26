from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> Self:

        return self

    async def __aexit__(self, *args):
        ...

    def get_session(self):
        return self._session

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()
