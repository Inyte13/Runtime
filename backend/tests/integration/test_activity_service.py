from datetime import date

import pytest
from app.core.exceptions.activity_exception import DefaultActivityDeletionError
from app.core.exceptions.generic_exception import ConflictError, NotFoundError
from app.repositories.activity_repository import activity_repository
from app.schemas.block_schema import BlockUpdate
from app.services.activity_service import activity_service
from app.services.base_service import get_or_raise
from app.services.block_service import block_service
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.block_factory import create_blocks
from tests.factories.category_factory import create_categories_with_activities
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_delete_activity_in_use(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 9, 3)
  categories_with_activities_map = await create_categories_with_activities(
    test_session, user.id
  )
  blocks = await create_blocks(test_session, user, test_date, count=10)
  _, activity_0 = categories_with_activities_map[0]
  activity_0_0 = activity_0[0]

  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )
  with pytest.raises(ConflictError):
    await activity_service.delete(test_session, user, activity_0_0.id)


@pytest.mark.asyncio
async def test_delete_default_activity(test_session: AsyncSession):
  user = await create_user(test_session)
  assert user.default_activity_id is not None
  default_activity = await activity_repository.get(
    test_session, user.default_activity_id, user.id
  )
  assert default_activity is not None
  with pytest.raises(DefaultActivityDeletionError):
    await activity_service.delete(test_session, user, default_activity.id)


@pytest.mark.asyncio
async def test_delete_activity_successfully(test_session: AsyncSession):
  user = await create_user(test_session)
  test_date = date(2026, 9, 3)
  categories_with_activities_map = await create_categories_with_activities(
    test_session, user.id
  )
  blocks = await create_blocks(test_session, user, test_date, count=10)
  _, activity_0 = categories_with_activities_map[0]
  activity_0_0 = activity_0[0]
  _, activity_1 = categories_with_activities_map[1]
  activity_1_0 = activity_1[0]

  await block_service.update(
    test_session,
    user.id,
    BlockUpdate(activity_id=activity_0_0.id),
    blocks[0].id,
  )

  await activity_service.delete(test_session, user, activity_1_0.id)
  with pytest.raises(NotFoundError):
    await get_or_raise(
      test_session, activity_repository, activity_1_0.id, user.id
    )
