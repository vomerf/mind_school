from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from apps.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)

async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
