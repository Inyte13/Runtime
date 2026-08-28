from collections.abc import AsyncIterator

import pytest_asyncio
from alembic import command
from alembic.config import Config
from app.core.settings import get_settings
from sqlalchemy import Connection, NullPool, text
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)


@pytest_asyncio.fixture(
  scope='session',
  loop_scope='session',
)  # Solo quiero que corra una vez por testing
async def ensure_test_database() -> AsyncIterator[None]:
  engine_postgres = create_async_engine(
    get_settings().DATABASE_ADMIN_URL,
    isolation_level='AUTOCOMMIT',
    poolclass=NullPool,  # Para que abra una conexión nueva cada vez que pidan
  )

  async with engine_postgres.connect() as connection:
    result = await connection.execute(
      text('SELECT 1 FROM pg_database WHERE datname = :database_name'),
      {'database_name': get_settings().POSTGRES_DB_TEST},
    )

    if result.scalar_one_or_none() is None:
      await connection.execute(
        text(f'CREATE DATABASE {get_settings().POSTGRES_DB_TEST}')
      )

  await engine_postgres.dispose()
  yield


engine_test = create_async_engine(
  get_settings().DATABASE_TEST_URL,
  echo=False,
  pool_pre_ping=True,  # Verifica la conexión antes de usarla, si está caída la descarta y abre una nueva en su lugar
  poolclass=NullPool,  # Para que abra una conexión nueva cada vez que pidan
)

TestSessionFactory = async_sessionmaker(
  engine_test, class_=AsyncSession, expire_on_commit=False
)


def do_run_migrations_test(
  connection: Connection, alembic_config: Config
) -> None:
  alembic_config.attributes['connection'] = connection
  command.upgrade(alembic_config, 'head')


@pytest_asyncio.fixture(scope='session', loop_scope='session')
async def run_migrations_test(ensure_test_database: None):
  alembic_config = Config('alembic.ini')

  async with engine_test.begin() as connection:
    await connection.run_sync(do_run_migrations_test, alembic_config)


@pytest_asyncio.fixture
async def test_session(run_migrations_test: None):
  async with TestSessionFactory() as session:
    try:
      yield session
    finally:
      await session.rollback()
