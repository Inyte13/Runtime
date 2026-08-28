from datetime import date

import pytest
from app.models.day import Day
from app.schemas.day_schema import DayUpdate
from app.services.day_service import day_service
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.block_factory import create_block
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_get_or_create_creates_day_when_missing(
  test_session: AsyncSession,
):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await day_service.get_or_create(test_session, test_date, user.id)
  day_bd = await test_session.get(Day, (test_date, user.id))
  assert day_bd is not None
  assert day_bd.date == test_date
  assert day_bd.user_id == user.id


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
  day_with_blocks = await day_service.get_with_blocks(
    test_session, user.id, test_date
  )
  assert len(day_with_blocks.blocks) == 1


@pytest.mark.asyncio
async def test_upsert_creates_day_when_missing(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  title = 'Hola mundo'
  await day_service.upsert(
    test_session, user.id, DayUpdate(title=title), test_date
  )
  day_bd = await test_session.get(Day, (test_date, user.id))
  assert day_bd is not None
  assert day_bd.date == test_date
  assert day_bd.user_id == user.id
  assert day_bd.title == title


@pytest.mark.asyncio
async def test_upsert_update_existing_day(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await day_service.get_or_create(test_session, test_date, user.id)
  title = 'Chau mundo'
  await day_service.upsert(
    test_session, user.id, DayUpdate(title=title), test_date
  )
  day_bd = await test_session.get(Day, (test_date, user.id))
  assert day_bd is not None
  assert day_bd.title == title
