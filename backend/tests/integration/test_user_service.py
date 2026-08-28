import pytest
from app.core.constants import (
  DEFAULT_ACTIVITY_NAME,
  DEFAULT_CATEGORY_COLOR,
  DEFAULT_CATEGORY_NAME,
)
from app.models.activity import Activity
from app.models.category import Category
from pydantic_extra_types import Color
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.user_factory import create_user


@pytest.mark.asyncio
async def test_create_user(
  test_session: AsyncSession,
):
  user = await create_user(test_session)

  categories_result = await test_session.execute(
    select(Category).where(Category.user_id == user.id)
  )
  categories = categories_result.scalars().all()

  activities_result = await test_session.execute(
    select(Activity).where(Activity.user_id == user.id)
  )
  activities = activities_result.scalars().all()

  assert user.id is not None
  assert user.activity_default_id is not None

  assert len(categories) == 1
  assert len(activities) == 1

  assert categories[0].name == DEFAULT_CATEGORY_NAME
  assert categories[0].color == Color(DEFAULT_CATEGORY_COLOR)
  assert activities[0].name == DEFAULT_ACTIVITY_NAME
  assert activities[0].category_id == categories[0].id
  assert activities[0].id == user.activity_default_id
