import uuid
from collections.abc import Sequence
from datetime import date

from app.models.activity import Activity
from app.models.block import Block
from app.models.day import Day
from app.models.hidden_activity import HiddenActivity
from app.schemas.day_schema import DayUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class DayRepository:
  async def create(self, session: AsyncSession, day: Day) -> Day:
    session.add(day)
    await session.flush()
    return day

  async def get(
    self, session: AsyncSession, date: date, user_id: uuid.UUID
  ) -> Day | None:
    # Solo para pk compuesta
    return await session.get(Day, (date, user_id))

  async def get_with_blocks(
    self, session: AsyncSession, date: date, user_id: uuid.UUID
  ) -> Day | None:
    statement = (
      select(Day)
      .where(Day.date == date)
      .where(Day.user_id == user_id)
      .options(selectinload(Day.blocks))
    )
    result = await session.execute(statement)
    return result.scalars().first()

  async def get_by_range(
    self,
    session: AsyncSession,
    date_from: date,
    date_to: date,
    user_id: uuid.UUID,
  ) -> Sequence[Day]:
    statement = (
      select(Day)
      .where(Day.user_id == user_id)
      .where(date_from <= Day.date)
      .where(Day.date <= date_to)
      .order_by(Day.date)
    )
    result = await session.execute(statement)
    return result.scalars().all()

  async def get_calendar_data_by_range(
    self,
    session: AsyncSession,
    date_from: date,
    date_to: date,
    user_id: uuid.UUID,
  ) -> Sequence[tuple[date, uuid.UUID, float, str | None, uuid.UUID]]:
    # (date, UUID_actividad, 0.5, "Revisar documentación", UUID_categoria)
    subquery = select(HiddenActivity.activity_id).where(
      HiddenActivity.user_id == user_id
    )
    statement = (
      select(
        Block.date,
        Block.activity_id,
        Block.duration,
        Block.description,
        Activity.category_id,
      )
      .join(Activity)
      .where(Block.user_id == user_id)
      .where(date_from <= Block.date)
      .where(Block.date <= date_to)
      .where(Activity.id.notin_(subquery))
      .order_by(Block.date)
    )
    result_with_row = await session.execute(statement)
    result: list[tuple[date, uuid.UUID, float, str | None, uuid.UUID]] = []
    for row in result_with_row.all():
      result.append(tuple(row))
    return result

  async def update(
    self, session: AsyncSession, day_obj: Day, day: DayUpdate
  ) -> Day:
    update_data = day.model_dump(exclude_unset=True)
    # Parseamos de dict directamente update los campos
    for field, value in update_data.items():
      # SQLAlchemy compara el valor con el nuevo, solo manda si hay cambios
      setattr(day_obj, field, value)
    await session.flush()
    return day_obj

  async def delete(self, session: AsyncSession, day: Day) -> None:
    await session.delete(day)


day_repository = DayRepository()
