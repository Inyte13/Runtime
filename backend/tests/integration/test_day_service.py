from datetime import date

import pytest
from app.core.constants import GRANULARITY_HOURS
from app.models.day import Day
from app.schemas.block_schema import BlockUpdate
from app.schemas.day_schema import DayUpdate
from app.services.block_service import block_service
from app.services.day_service import day_service
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.block_factory import create_block, create_blocks
from tests.factories.category_factory import create_categories_with_activities
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_get_or_create_creates_day_when_missing(
  test_session: AsyncSession,
):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await day_service.get_or_create(test_session, test_date, user.id)
  day = await test_session.get(Day, (test_date, user.id))
  assert day is not None
  assert day.date == test_date
  assert day.user_id == user.id


@pytest.mark.asyncio
async def test_get_or_create_returns_existing_day(
  test_session: AsyncSession,
):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  day_one = await day_service.get_or_create(test_session, test_date, user.id)
  day_two = await day_service.get_or_create(test_session, test_date, user.id)
  assert day_one is day_two
  assert day_one.date == test_date
  assert day_one.user_id == user.id


@pytest.mark.asyncio
async def test_get_with_blocks_success(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await create_block(test_session, user, test_date)
  day = await day_service.get_with_blocks(test_session, user.id, test_date)
  assert len(day.blocks) == 1


@pytest.mark.asyncio
async def test_get_calendar_by_range(test_session: AsyncSession):
  user = await create_user(test_session)
  test_first_date = date(2026, 5, 20)
  test_thirt_date = date(2026, 5, 22)
  day_thirt = await day_service.get_or_create(
    test_session, test_thirt_date, user.id
  )
  blocks = await create_blocks(
    test_session,
    user,
    test_first_date,
    count=10,
    overrides_duration={3: GRANULARITY_HOURS * 2, 8: GRANULARITY_HOURS * 2},
    overrides_description={2: 'Descripción 0', 3: 'Descripción 1'},
  )
  categories_with_activities = await create_categories_with_activities(
    test_session,
    user.id,
    overrides_activities_per_category={0: 2},
    hidden_activity_by_category={0: [0]},
  )
  # Category 0
  # Activity 0.0, oculta
  # Activity 0.1

  # Category 1
  # Activity 1.0
  _, activity_0 = categories_with_activities[0]
  activity_0_0 = activity_0[0]
  activity_0_1 = activity_0[1]
  _, activity_1 = categories_with_activities[1]
  activity_1_0 = activity_1[0]
  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )
  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_1.id),
    blocks[1].id,
  )
  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_1.id),
    blocks[2].id,
  )
  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_1_0.id),
    blocks[3].id,
  )
  calendar_days = await day_service.get_calendar_by_range(
    test_session, user.id, test_first_date, test_thirt_date
  )
  calendar_activity_count = 0
  for category in calendar_days[0].categories:
    calendar_activity_count += len(category.activities)

  assert calendar_days[0].date == test_first_date
  assert calendar_days[1].date == day_thirt.date
  assert (
    len(calendar_days[0].categories)
    == len(categories_with_activities.keys()) + 1
  )
  assert calendar_activity_count == 3 - 1 + 1
  assert calendar_days[1].categories == []


@pytest.mark.asyncio
async def test_upsert_creates_day_when_missing(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  title = 'Hola mundo'
  await day_service.upsert(
    test_session, user.id, DayUpdate(title=title), test_date
  )
  day = await test_session.get(Day, (test_date, user.id))
  assert day is not None
  assert day.date == test_date
  assert day.user_id == user.id
  assert day.title == title


@pytest.mark.asyncio
async def test_upsert_update_existing_day(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await day_service.get_or_create(test_session, test_date, user.id)
  title = 'Chau mundo'
  await day_service.upsert(
    test_session, user.id, DayUpdate(title=title), test_date
  )
  day = await test_session.get(Day, (test_date, user.id))
  assert day is not None
  assert day.title == title
