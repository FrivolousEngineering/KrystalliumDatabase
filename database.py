import pathlib

# import fastapi
# import pydantic
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Boolean, Integer, String


DatabaseUrl = f"sqlite+aiosqlite:///{pathlib.Path(__file__).resolve().parent}/krystalium.db"


Base = sqlalchemy.ext.declarative.declarative_base()


class SampleBase(sqlalchemy.ext.declarative.AbstractConcreteBase, Base):
    id = Column(Integer, primary_key = True, index = True)
    rfid_id = Column(String, unique = True)
    strength = Column(Integer, nullable = False)


class RawSample(SampleBase):
    __tablename__ = "raw"

    positive_action = Column(String, nullable = False)
    positive_target = Column(String, nullable = False)
    negative_action = Column(String, nullable = False)
    negative_target = Column(String, nullable = False)

    depleted = Column(Boolean, default = False)


class RefinedSample(SampleBase):
    __tablename__ = "refined"

    primary_action = Column(String, nullable = False)
    primary_target = Column(String, nullable = False)
    secondary_action = Column(String, nullable = False)
    secondary_target = Column(String, nullable = False)


class BloodSample(SampleBase):
    __tablename__ = "blood"

    origin = Column(String, nullable = False)
    action = Column(String, nullable = False)
    target = Column(String, nullable = False)


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
