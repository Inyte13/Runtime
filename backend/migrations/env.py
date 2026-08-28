import asyncio
from typing import Literal

from alembic import context
from app.core.database import Base

# pyright: reportUnusedImport=false
from app.core.settings import get_settings
from app.models import (  # noqa: F401
  activity,
  block,
  category,
  day,
  hidden_activity,
  refresh_token,
  user,
)
from app.models.types import ColorType  # noqa: F401
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

config = context.config

if not config.get_main_option('sqlalchemy.url'):
  config.set_main_option(
    'sqlalchemy.url',
    get_settings().DATABASE_URL.replace('%', '%%'),
  )
target_metadata = Base.metadata


def run_migrations_offline() -> None:

  url = config.get_main_option('sqlalchemy.url')
  context.configure(
    url=url,
    target_metadata=target_metadata,
    literal_binds=True,
    dialect_opts={'paramstyle': 'named'},
  )

  with context.begin_transaction():
    context.run_migrations()


def render_item(
  type_: str, obj: object, autogen_context: object
) -> str | Literal[False]:
  if type_ == 'type' and isinstance(obj, ColorType):
    return 'sa.String(length=7)'
  return False


def do_run_migrations(connection: Connection) -> None:
  context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_item=render_item,
    compare_type=True,
    compare_server_default=True,
  )

  with context.begin_transaction():
    context.run_migrations()


async def run_async_migrations() -> None:

  connectable = async_engine_from_config(
    config.get_section(config.config_ini_section, {}),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool,
  )

  async with connectable.connect() as connection:
    await connection.run_sync(do_run_migrations)

  await connectable.dispose()


def run_migrations_online() -> None:
  connectable = config.attributes.get('connection', None)
  if connectable is not None:
    do_run_migrations(connectable)
  else:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
  run_migrations_offline()
else:
  run_migrations_online()
