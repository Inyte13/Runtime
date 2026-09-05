import uuid
from collections.abc import Sequence
from datetime import date

from app.core.exceptions.generic_exception import (
  InvalidDateRangeError,
  NotFoundError,
)
from app.models.day import Day
from app.repositories.block_repository import block_repository
from app.repositories.day_repository import day_repository
from app.schemas.activity_schema import ActivityCalendar
from app.schemas.block_schema import BlockResponse
from app.schemas.category_schema import CategoryCalendar
from app.schemas.day_schema import DayCalendar, DayResponseDetail, DayUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class DayService:
  def __init__(self):
    self.repository = day_repository

  async def get_or_create(
    self, session: AsyncSession, date: date, user_id: uuid.UUID
  ) -> Day:
    day = await day_repository.get(session, date, user_id)
    if day is None:
      day = await day_repository.create(
        session, Day(date=date, user_id=user_id)
      )
    return day

  async def get_with_blocks(
    self, session: AsyncSession, user_id: uuid.UUID, date: date
  ) -> DayResponseDetail:
    day = await self.repository.get(session, date, user_id)
    if day is None:
      raise NotFoundError()
    blocks = await block_repository.get_by_range(
      session,
      date,
      user_id,
    )
    block_responses: list[BlockResponse] = []

    for block in blocks:
      block_responses.append(BlockResponse.model_validate(block))
    return DayResponseDetail(
      date=day.date,
      title=day.title,
      blocks=block_responses,
    )

  def build_day_calendar(
    self,
    tuples: Sequence[tuple[date, uuid.UUID, float, str | None, uuid.UUID]],
    # (date, UUID_actividad, 0.5, "Revisar documentación", UUID_categoria)
    date: date,
    title: str | None = None,
  ) -> DayCalendar:
    categories_dict: dict[uuid.UUID, CategoryCalendar] = {}
    activities_dict: dict[uuid.UUID, ActivityCalendar] = {}
    total_duration = 0
    for tuple_ in tuples:
      _, activity_id, duration, description, category_id = tuple_

      total_duration += duration
      if category_id not in categories_dict:
        categories_dict[category_id] = CategoryCalendar(
          id=category_id, activities=[], duration=0
        )
      categories_dict[category_id].duration += duration

      if activity_id not in activities_dict:
        activity = ActivityCalendar(
          id=activity_id,
          duration=0,
          descriptions=[],
        )
        activities_dict[activity_id] = activity
        categories_dict[category_id].activities.append(activity)
      activities_dict[activity_id].duration += duration
      if description:
        activities_dict[activity_id].descriptions.append(description)

    categories = list(categories_dict.values())
    categories.sort(key=lambda category: category.duration, reverse=True)
    for category in categories:
      category.activities.sort(
        key=lambda activity: activity.duration, reverse=True
      )

    return DayCalendar(
      date=date,
      title=title,
      duration=total_duration,
      categories=categories,
    )

  async def get_calendar_by_range(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    date_from: date,
    date_to: date,
  ) -> list[DayCalendar]:
    if date_to < date_from:
      raise InvalidDateRangeError()
    if (date_to - date_from).days > 365:
      raise InvalidDateRangeError()

    days_bd = await self.repository.get_by_range(
      session, date_from, date_to, user_id
    )
    calendar_data = await self.repository.get_calendar_data_by_range(
      session, date_from, date_to, user_id
    )

    dict_calendar: dict[
      date, list[tuple[date, uuid.UUID, float, str | None, uuid.UUID]]
    ] = {}
    for tuple_ in calendar_data:
      date_ = tuple_[0]
      if date_ not in dict_calendar:
        dict_calendar[date_] = []
      dict_calendar[date_].append(tuple_)

    calendar_days: list[DayCalendar] = []
    for day_bd in days_bd:
      calendar_days.append(
        self.build_day_calendar(
          dict_calendar.get(day_bd.date, []), day_bd.date, day_bd.title
        )
      )
    return calendar_days

  async def upsert(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    day_update: DayUpdate,
    date: date,
  ) -> Day:
    day_bd = await self.repository.get(session, date, user_id)
    if day_bd is not None:
      return await self.repository.update(session, day_bd, day_update)
    data = day_update.model_dump(exclude_unset=True)
    new_day = Day(date=date, user_id=user_id, **data)
    return await self.repository.create(session, new_day)


day_service = DayService()
