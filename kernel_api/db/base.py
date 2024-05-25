from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta

from configs import CONFIG


metadata = MetaData()
BASE: DeclarativeMeta = declarative_base(metadata=metadata)

url_object = URL.create(
    drivername=CONFIG.DRIVERNAME,
    port=CONFIG.DB_PORT,
    username=CONFIG.DB_USERNAME,
    password=CONFIG.DB_PASSWORD,
    host=CONFIG.DB_HOST,
    database=CONFIG.DB_NAME,
    query={'application_name': 'KERNEL_API'}
)


engine = create_async_engine(
    url_object, echo=False
)


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(
            BASE.metadata.create_all
        )


async def clear_database() -> bool | None:
    async with engine.begin() as conn:
        await conn.run_sync(
            BASE.metadata.drop_all
        )
        await conn.run_sync(
            BASE.metadata.create_all
        )
        return True