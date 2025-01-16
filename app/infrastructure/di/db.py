from typing import AsyncIterable

from dishka import Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.infrastructure.db.uow import UnitOfWork
from app.infrastructure.config import DatabaseConfig


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: DatabaseConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(config.make_connection_url())
        yield engine
        await engine.dispose()
        
    @provide
    async def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)
    
    @provide(scope=Scope.REQUEST)
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    uow = provide(UnitOfWork, scope=Scope.REQUEST)
    
