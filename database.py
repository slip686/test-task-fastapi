from sqlalchemy import create_engine

from settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from models.models import Base, TrackPointModel, VehicleModel

config = get_settings()
engine = AsyncEngine(create_engine(config.db.dsn, echo=True, pool_pre_ping=True))
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
