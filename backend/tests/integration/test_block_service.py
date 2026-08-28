from datetime import date, datetime, time, timedelta

import pytest
from app.core.constants import GRANULARITY_HOURS
from app.models.block import Block
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.block_factory import create_block
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_create_block_end_position(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  block_create = await create_block(test_session, user, test_date)
  block_bd = await test_session.get(Block, block_create.id)
  hour_end = (
    datetime.combine(test_date, time(0, 0)) + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  assert block_bd is not None
  assert block_bd.date == test_date
  assert block_bd.hour == time(0, 0)
  assert block_bd.hour_end == hour_end
  assert block_bd.duration == GRANULARITY_HOURS
  assert block_bd.description is None
  assert block_bd.activity_id == user.activity_default_id
