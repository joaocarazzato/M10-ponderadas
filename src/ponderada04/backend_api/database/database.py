from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres_pw@db_async:5432/postgres_database"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)

db = declarative_base()

async def get_async_session():
    async with SessionLocal() as session:
        yield session
        await session.close()