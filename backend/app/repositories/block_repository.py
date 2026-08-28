import uuid
from collections.abc import Sequence
from datetime import date, time

from app.models.block import Block
from app.repositories.base_repository import BaseRepository
from app.schemas.block_schema import BlockUpdate
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class BlockRepository(BaseRepository[Block, BlockUpdate]):
  async def get_last(
    self, session: AsyncSession, date: date, user_id: uuid.UUID
  ) -> Block | None:
    statement = (
      select(Block)
      .where(Block.date == date)
      .where(Block.user_id == user_id)
      .order_by(desc(Block.hour))
    )
    result = await session.execute(statement)
    # scalars: extrae el primer elemento de cada tupla
    return result.scalars().first()

  async def get_by_range(
    self,
    session: AsyncSession,
    date: date,
    user_id: uuid.UUID,
    hour_from: time | None = None,
    hour_to: time | None = None,
    exclude_hour_from: bool = False,
    exclude_hour_to: bool = False,
  ) -> Sequence[Block]:
    statement = (
      select(Block)
      .where(Block.date == date)
      .where(Block.user_id == user_id)
      .order_by(Block.hour)
    )
    if hour_from is not None:
      if exclude_hour_from:
        statement = statement.where(hour_from < Block.hour)
      else:
        statement = statement.where(hour_from <= Block.hour)
    if hour_to is not None:
      if exclude_hour_to:
        statement = statement.where(Block.hour < hour_to)
      else:
        statement = statement.where(Block.hour <= hour_to)
    result = await session.execute(statement)
    # scalars: pextrae el primer elemento de cada tupla
    return result.scalars().all()


block_repository = BlockRepository(Block)
