from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from consts_secrets import db_username, db_password, db_name
from contextlib import asynccontextmanager

PSQL_QUERY_ALLOWED_MAX_ARGS = 32767


def async_session_generator():
    return async_sessionmaker(bind=get_db_engine(), sync_session_class=sessionmaker())


def get_db_engine() -> AsyncEngine:
    return create_async_engine(f'postgresql+asyncpg://{db_username}:{db_password}@db/{db_name}', pool_pre_ping=True)


def get_db_session():
    return async_sessionmaker(get_db_engine())


@asynccontextmanager
async def get_session() -> AsyncSession:
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


async def pg_bulk_insert(
        session: AsyncSession, table,
        data, statement_modifier=None,
        # insert=insert_
):
    if statement_modifier is None:
        def statement_modifier(s):
            return s

    complete_batches = []

    current_batch = []
    current_count = 0
    for row in data:
        params_count = len(row)
        current_count += params_count
        if current_count >= PSQL_QUERY_ALLOWED_MAX_ARGS:
            complete_batches.append(current_batch)
            current_batch = [row]
            current_count = params_count
        else:
            current_batch.append(row)
    if len(current_batch) > 0:
        complete_batches.append(current_batch)

    for batch in complete_batches:
        statement = statement_modifier(
            insert(table)
            .values(batch)
        )
        await session.execute(statement)
