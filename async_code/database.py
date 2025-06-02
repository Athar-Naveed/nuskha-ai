import os
import asyncpg
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from schema.transactions import Base

load_dotenv()

connection_uri:str = os.getenv("DB_CONNECTION_URL")

engine = create_async_engine(connection_uri,echo=True)
async_session = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as error:
        print(f"Error! {error}")


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
        