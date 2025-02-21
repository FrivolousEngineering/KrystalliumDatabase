import pathlib

# import fastapi
# import pydantic
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Boolean, Integer, String


DatabaseUrl = f"sqlite+aiosqlite:///{pathlib.Path(__file__).resolve().parent}/krystalium.db"





def async_session() -> sqlalchemy.orm.sessionmaker:
    engine = sqlalchemy.ext.asyncio.create_async_engine(url = sqlalchemy.engine.make_url(DatabaseUrl))
    return sqlalchemy.orm.sessionmaker(bind = engine, class_ = sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit = False)


class Connector:
    @classmethod
    async def get_session(cls):
        session = async_session()
        async with session() as db_session:
            yield db_session
            await db_session.rollback()


async def sqlalchemy_init():
    engine = sqlalchemy.ext.asyncio.create_async_engine(url = sqlalchemy.engine.make_url(DatabaseUrl))
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
