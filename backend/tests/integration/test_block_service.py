from datetime import date, datetime, time, timedelta

import pytest
from app.core.constants import GRANULARITY_HOURS
from app.core.exceptions.generic_exception import ConflictError
from app.core.exceptions.time_exception import TimeBoundaryError
from app.repositories.block_repository import block_repository
from app.schemas.block_schema import RelativePosition
from app.services.block_service import block_service
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.block_factory import create_block, create_blocks
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_create_end_zero_blocks(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  block = await create_block(test_session, user, test_date)
  hour_end = (
    datetime.combine(test_date, time(0, 0)) + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  assert block.hour == time(0, 0)
  assert block.hour_end == hour_end
  assert block.activity_id == user.default_activity_id


@pytest.mark.asyncio
async def test_create_end_existing_blocks(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=10)
  block = await create_block(test_session, user, test_date)
  hour = blocks[9].hour_end
  hour_end = (
    datetime.combine(test_date, hour) + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  assert block.hour == hour
  assert block.hour_end == hour_end
  assert block.activity_id == user.default_activity_id


@pytest.mark.asyncio
async def test_create_end_full(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  await create_blocks(test_session, user, test_date, count=48)
  with pytest.raises(TimeBoundaryError):
    await create_block(test_session, user, test_date)


@pytest.mark.asyncio
async def test_create_after_middle_block(
  test_session: AsyncSession,
):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=5)
  target_block = blocks[3]
  block = await create_block(
    test_session,
    user,
    test_date,
    placement=RelativePosition(position='after', target_id=target_block.id),
  )
  hour_end = (
    datetime.combine(test_date, target_block.hour_end)
    + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  assert block.hour == target_block.hour_end
  assert block.hour_end == hour_end
  assert block.hour_end == blocks[4].hour
  assert block.activity_id == user.default_activity_id


@pytest.mark.asyncio
async def test_create_after_middle_block_full(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=48)
  target_block = blocks[24]
  with pytest.raises(TimeBoundaryError):
    await create_block(
      test_session,
      user,
      test_date,
      placement=RelativePosition(position='after', target_id=target_block.id),
    )


@pytest.mark.asyncio
async def test_create_after_last_block(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=7)
  target_block = blocks[6]
  block = await create_block(
    test_session,
    user,
    test_date,
    placement=RelativePosition(position='after', target_id=target_block.id),
  )
  hour_end = (
    datetime.combine(test_date, target_block.hour_end)
    + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  assert block.hour == target_block.hour_end
  assert block.hour_end == hour_end
  assert block.activity_id == user.default_activity_id


@pytest.mark.asyncio
async def test_create_before_middle_block(
  test_session: AsyncSession,
):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=27)
  target_block = blocks[10]
  hour = target_block.hour
  hour_end = (
    datetime.combine(test_date, target_block.hour)
    + timedelta(hours=GRANULARITY_HOURS)
  ).time()
  # Van antes porque modifica al propio target_block
  block = await create_block(
    test_session,
    user,
    test_date,
    placement=RelativePosition(position='before', target_id=target_block.id),
  )
  assert block.hour == hour
  assert block.hour_end == hour_end
  assert block.activity_id == user.default_activity_id


@pytest.mark.asyncio
async def test_create_before_middle_block_full(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(test_session, user, test_date, count=48)
  target_block = blocks[17]
  with pytest.raises(TimeBoundaryError):
    await create_block(
      test_session,
      user,
      test_date,
      placement=RelativePosition(position='before', target_id=target_block.id),
    )


@pytest.mark.asyncio
async def test_reorder_different_order(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  original_blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=10,
    overrides_duration={
      3: GRANULARITY_HOURS * 3,
      4: GRANULARITY_HOURS * 4,
      7: GRANULARITY_HOURS * 2,
    },
  )

  rearranged_blocks = await block_service.reorder(
    test_session,
    user.id,
    test_date,
    [
      original_blocks[0].id,
      original_blocks[4].id,
      original_blocks[7].id,
      original_blocks[1].id,
      original_blocks[2].id,
      original_blocks[8].id,
      original_blocks[3].id,
      original_blocks[9].id,
      original_blocks[6].id,
      original_blocks[5].id,
    ],
  )

  expected_hour = datetime.combine(test_date, time(0, 0))

  for block in rearranged_blocks:
    assert block.hour == expected_hour.time()
    expected_hour += timedelta(hours=block.duration)
    assert block.hour_end == expected_hour.time()


@pytest.mark.asyncio
async def test_reorder_current_order(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  original_blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=5,
    overrides_duration={
      3: GRANULARITY_HOURS * 3,
      4: GRANULARITY_HOURS * 4,
    },
  )

  rearranged_blocks = await block_service.reorder(
    test_session,
    user.id,
    test_date,
    [
      original_blocks[0].id,
      original_blocks[1].id,
      original_blocks[2].id,
      original_blocks[3].id,
      original_blocks[4].id,
    ],
  )
  assert original_blocks == rearranged_blocks


@pytest.mark.asyncio
async def test_reorder_different_block_ids(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  original_blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=5,
    overrides_duration={
      3: GRANULARITY_HOURS * 3,
      4: GRANULARITY_HOURS * 4,
    },
  )
  with pytest.raises(ConflictError):
    await block_service.reorder(
      test_session,
      user.id,
      test_date,
      [
        original_blocks[0].id,
        original_blocks[1].id,
        original_blocks[2].id,
        original_blocks[4].id,
        original_blocks[4].id,
      ],
    )


@pytest.mark.asyncio
async def test_reorder_different_number_block_ids(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  original_blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=5,
    overrides_duration={
      3: GRANULARITY_HOURS * 3,
      4: GRANULARITY_HOURS * 4,
    },
  )
  with pytest.raises(ConflictError):
    await block_service.reorder(
      test_session,
      user.id,
      test_date,
      [
        original_blocks[0].id,
        original_blocks[1].id,
        original_blocks[2].id,
        original_blocks[3].id,
        original_blocks[4].id,
        original_blocks[4].id,
      ],
    )


@pytest.mark.asyncio
async def test_delete_middle_block(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=30,
    overrides_duration={
      13: GRANULARITY_HOURS * 2,
      14: GRANULARITY_HOURS * 3,
      15: GRANULARITY_HOURS * 2,
      16: GRANULARITY_HOURS * 4,
      18: GRANULARITY_HOURS * 4,
    },
  )
  block_removed = blocks[15]
  next_block = blocks[16]
  last_block = blocks[29]
  hour_end = (
    datetime.combine(test_date, last_block.hour_end)
    - timedelta(hours=block_removed.duration)
  ).time()
  await block_service.delete(test_session, user.id, block_removed.id)
  assert next_block.hour == block_removed.hour
  assert last_block.hour_end == hour_end


@pytest.mark.asyncio
async def test_delete_last_block(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 5, 20)
  blocks = await create_blocks(
    test_session,
    user,
    test_date,
    count=30,
  )
  block_previously = blocks[28]
  block_removed = blocks[29]
  await block_service.delete(test_session, user.id, block_removed.id)
  last_block = await block_repository.get_last(test_session, test_date, user.id)

  assert last_block is not None
  assert last_block.id == block_previously.id
