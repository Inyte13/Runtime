from datetime import date
from typing import Annotated

from app.core.settings import get_settings
from fastapi import Depends, Path, Query
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass


engine = create_async_engine(
  get_settings().DATABASE_URL,
  echo=False,
  pool_pre_ping=True,  # Verifica la conexión antes de usarla, si está caída la descarta y abre una nueva en su lugar
)

SessionFactory = async_sessionmaker(
  engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
  async with SessionFactory() as session:
    try:
      yield session
      await session.commit()
    except Exception:
      await session.rollback()
      raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]

PathDate = Annotated[
  date,
  Path(..., openapi_examples={'example': {'value': date.today().isoformat()}}),
]
QueryDate = Annotated[
  date,
  Query(..., openapi_examples={'example': {'value': date.today().isoformat()}}),
]
