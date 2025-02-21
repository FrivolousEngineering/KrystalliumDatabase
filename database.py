import pathlib

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import sqlalchemy


DatabaseUrl = f"sqlite+aiosqlite:///{pathlib.Path(__file__).resolve().parent}/krystalium.db"


engine = sqlalchemy.ext.asyncio.create_async_engine(url = sqlalchemy.engine.make_url(DatabaseUrl))


async def get_session() -> AsyncSession:
    session = sqlalchemy.orm.sessionmaker(bind = engine, class_ = AsyncSession, expire_on_commit = False)
    async with session() as db_session:
        yield db_session
        await db_session.rollback()


async def sqlalchemy_init():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
