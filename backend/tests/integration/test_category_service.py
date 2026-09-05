from datetime import date

import pytest
from app.core.exceptions.category_exception import DefaultCategoryDeletionError
from app.core.exceptions.generic_exception import ConflictError, NotFoundError
from app.repositories.activity_repository import activity_repository
from app.repositories.category_repository import category_repository
from app.schemas.block_schema import BlockUpdate
from app.services.base_service import get_or_raise
from app.services.block_service import block_service
from app.services.category_service import category_service
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.block_factory import create_blocks
from tests.factories.category_factory import create_categories_with_activities
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_get_all_with_activities(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 9, 3)
  categories_with_activities_map = await create_categories_with_activities(
    test_session,
    user.id,
    count=3,
    activities_per_category=3,
    overrides_activities_per_category={
      2: 4,
    },
    hidden_activity_by_category={0: [0, 1]},
  )

  blocks = await create_blocks(test_session, user, test_date, count=10)
  category_0, activity_0 = categories_with_activities_map[0]
  activity_0_0 = activity_0[0]
  activity_0_1 = activity_0[1]
  activity_0_2 = activity_0[2]
  category_1, activity_1 = categories_with_activities_map[1]
  activity_1_0 = activity_1[0]
  activity_1_1 = activity_1[1]
  activity_1_2 = activity_1[2]
  category_2, activity_2 = categories_with_activities_map[2]
  activity_2_0 = activity_2[0]
  activity_2_1 = activity_2[1]
  activity_2_2 = activity_2[2]
  activity_2_3 = activity_2[3]

  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )
  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_1_1.id),
    blocks[1].id,
  )
  categories_with_activities = await category_service.get_all_with_activities(
    test_session, user
  )
  category_bd_0 = categories_with_activities[0]
  activity_bd_0_0 = category_bd_0.activities[0]
  activity_bd_0_1 = category_bd_0.activities[1]
  activity_bd_0_2 = category_bd_0.activities[2]

  category_bd_1 = categories_with_activities[1]
  activity_bd_1_0 = category_bd_1.activities[0]
  activity_bd_1_1 = category_bd_1.activities[1]
  activity_bd_1_2 = category_bd_1.activities[2]

  category_bd_2 = categories_with_activities[2]
  activity_bd_2_0 = category_bd_2.activities[0]
  activity_bd_2_1 = category_bd_2.activities[1]
  activity_bd_2_2 = category_bd_2.activities[2]
  activity_bd_2_3 = category_bd_2.activities[3]

  assert category_0.id == category_bd_0.id
  assert category_1.id == category_bd_1.id
  assert category_2.id == category_bd_2.id
  assert category_bd_0.deletable is False
  assert category_bd_1.deletable is False
  assert category_bd_2.deletable is True

  assert activity_0_0.id == activity_bd_0_0.id
  assert activity_bd_0_0.deletable is False
  assert activity_0_1.id == activity_bd_0_1.id
  assert activity_bd_0_1.deletable is True
  assert activity_0_2.id == activity_bd_0_2.id
  assert activity_bd_0_2.deletable is True

  assert activity_1_0.id == activity_bd_1_0.id
  assert activity_bd_1_0.deletable is True
  assert activity_1_1.id == activity_bd_1_1.id
  assert activity_bd_1_1.deletable is False
  assert activity_1_2.id == activity_bd_1_2.id
  assert activity_bd_1_2.deletable is True

  assert activity_2_0.id == activity_bd_2_0.id
  assert activity_bd_2_0.deletable is True
  assert activity_2_1.id == activity_bd_2_1.id
  assert activity_bd_2_1.deletable is True
  assert activity_2_2.id == activity_bd_2_2.id
  assert activity_bd_2_2.deletable is True
  assert activity_2_3.id == activity_bd_2_3.id
  assert activity_bd_2_3.deletable is True


@pytest.mark.asyncio
async def test_delete_category_with_used_activities(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 9, 3)
  categories_with_activities_map = await create_categories_with_activities(
    test_session, user.id
  )
  blocks = await create_blocks(test_session, user, test_date, count=10)
  category_0, activity_0 = categories_with_activities_map[0]
  activity_0_0 = activity_0[0]

  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )
  with pytest.raises(ConflictError):
    await category_service.delete(test_session, user, category_0.id)


@pytest.mark.asyncio
async def test_delete_default_category(test_session: AsyncSession):
  user = await create_user(test_session)
  assert user.default_activity_id is not None
  default_activity = await activity_repository.get(
    test_session, user.default_activity_id, user.id
  )
  assert default_activity is not None
  default_category = await category_repository.get(
    test_session, default_activity.category_id, user.id
  )
  assert default_category is not None
  with pytest.raises(DefaultCategoryDeletionError):
    await category_service.delete(test_session, user, default_category.id)


@pytest.mark.asyncio
async def test_delete_category_successfully(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 9, 3)
  categories_with_activities_map = await create_categories_with_activities(
    test_session, user.id
  )
  blocks = await create_blocks(test_session, user, test_date, count=10)
  _, activity_0 = categories_with_activities_map[0]
  activity_0_0 = activity_0[0]
  category_1, activity_1 = categories_with_activities_map[1]
  activity_1_0 = activity_1[0]

  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )

  await category_service.delete(test_session, user, category_1.id)
  with pytest.raises(NotFoundError):
    await get_or_raise(
      test_session, category_repository, category_1.id, user.id
    )
  with pytest.raises(NotFoundError):
    await get_or_raise(
      test_session, activity_repository, activity_1_0.id, user.id
    )
