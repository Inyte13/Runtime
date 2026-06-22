from datetime import date
from typing import Annotated

from app.core.settings import settings
from fastapi import Depends, Path, Query
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
  settings.DATABASE_URL,
  echo=False,
  pool_pre_ping=True,  # Verifica la conexión antes de usarla
)

AsyncSessionLocal = async_sessionmaker(
  engine,
  class_=AsyncSession,
  expire_on_commit=False,
)


class Base(DeclarativeBase):
  pass


async def get_session():
  """Dependency for database session."""
  async with AsyncSessionLocal() as session:
    try:
      yield session
      await session.commit()
    except Exception:
      await session.rollback()
      raise
    finally:
      await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]

PathDate = Annotated[
  date,
  Path(..., openapi_examples={'example': {'value': date.today().isoformat()}}),
]
QueryDate = Annotated[
  date,
  Query(..., openapi_examples={'example': {'value': date.today().isoformat()}}),
]
