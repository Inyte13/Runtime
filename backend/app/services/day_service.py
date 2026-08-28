import uuid
from collections.abc import Sequence
from datetime import date

from app.core.exceptions.generic_exception import (
  InvalidDateRangeError,
  NotFoundError,
)
from app.models.day import Day
from app.repositories.day_repository import day_repository
from app.schemas.activity_schema import ActivityCalendar
from app.schemas.category_schema import CategoryCalendar
from app.schemas.day_schema import DayCalendar, DayUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class DayService:
  def __init__(self):
    self.repository = day_repository

  async def get_or_create(
    self, session: AsyncSession, date: date, user_id: uuid.UUID
  ) -> Day:
    day = await day_repository.get(session, date, user_id)
    if not day:
      day = await day_repository.create(
        session, Day(date=date, user_id=user_id)
      )
    return day

  async def get_with_blocks(
    self, session: AsyncSession, user_id: uuid.UUID, date: date
  ) -> Day:
    day = await self.repository.get_with_blocks(session, date, user_id)
    if not day:
      raise NotFoundError()
    return day

  def build_day_calendar(
    self,
    tuples: Sequence[tuple[date, uuid.UUID, float, str | None, uuid.UUID]],
    # (date, UUID_actividad, 0.5, "Revisar documentación", UUID_categoria)
    date: date,
    title: str | None = None,
  ) -> DayCalendar:
    categories_dict: dict[uuid.UUID, CategoryCalendar] = {}
    activities_dict: dict[uuid.UUID, ActivityCalendar] = {}

    for tuple_ in tuples:
      _, activity_id, duration, description, category_id = tuple_
      if category_id not in categories_dict:
        categories_dict[category_id] = CategoryCalendar(
          id=category_id, activities=[], duration=duration
        )
      else:
        categories_dict[category_id].duration += duration

      if activity_id not in activities_dict:
        activity = ActivityCalendar(
          id=activity_id,
          duration=duration,
          descriptions=[description] if description else [],
        )
        activities_dict[activity_id] = activity
        categories_dict[category_id].activities.append(activity)
      else:
        activities_dict[activity_id].duration += duration
        if description:
          activities_dict[activity_id].descriptions.append(description)

    categories = list(categories_dict.values())
    categories.sort(key=lambda category: category.duration, reverse=True)
    for category in categories_dict.values():
      category.activities.sort(
        key=lambda activity: activity.duration, reverse=True
      )

    return DayCalendar(
      date=date,
      title=title,
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
    if date_to == date_from:
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
      if date_ in dict_calendar:
        dict_calendar[date_].append(tuple_)
      else:
        dict_calendar[date_] = [tuple_]

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
    if day_bd:
      return await self.repository.update(session, day_bd, day_update)
    data = day_update.model_dump(exclude_unset=True)
    new_day = Day(date=date, user_id=user_id, **data)
    return await self.repository.create(session, new_day)

  async def delete(
    self, session: AsyncSession, user_id: uuid.UUID, date: date
  ) -> None:
    day = await self.repository.get(session, date, user_id)
    if not day:
      raise NotFoundError()
    return await self.repository.delete(session, day)


day_service = DayService()
