from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.repositories.uow import UnitOfWork


async def create_uow(sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            async with UnitOfWork(session) as uow:
                yield uow
