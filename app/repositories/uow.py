from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository


class UnitOfWork:
    _session: AsyncSession

    users: UserRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> Self:
        self.users = UserRepository(self._session)

        return self

    async def __aexit__(self, *args):
        ...

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()
