import uuid

from app.core.constants import DEFAULT_CATEGORY_COLOR
from app.models.activity import Activity
from app.models.category import Category
from app.models.hidden_activity import HiddenActivity
from pydantic_extra_types import Color
from sqlalchemy.ext.asyncio import AsyncSession


async def create_categories_with_activities(
  session: AsyncSession,
  user_id: uuid.UUID,
  count: int = 2,
  activities_per_category: int = 1,
  overrides_activities_per_category: dict[int, int] | None = None,
  hidden_activity_by_category: dict[int, list[int]] | None = None,
) -> dict[int, tuple[Category, list[Activity]]]:

  overrides_activities_per_category = (
    {}
    if overrides_activities_per_category is None
    else overrides_activities_per_category
  )
  categories_with_activities: dict[int, tuple[Category, list[Activity]]] = {}
  activities_to_hide: list[Activity] = []
  for i in range(count):
    category = Category(
      user_id=user_id,
      name=f'Categoria {i}',
      color=Color(DEFAULT_CATEGORY_COLOR),
    )
    session.add(category)
    await session.flush()

    activities_count = overrides_activities_per_category.get(
      i, activities_per_category
    )
    hidden_activity_indexes = (
      hidden_activity_by_category.get(i, [])
      if hidden_activity_by_category is not None
      else []
    )
    categories_with_activities[i] = (category, [])
    for j in range(activities_count):
      activity = Activity(
        user_id=user_id,
        category_id=category.id,
        name=f'Actividad {i}.{j}',
      )
      session.add(activity)
      if j in hidden_activity_indexes:
        activities_to_hide.append(activity)
      categories_with_activities[i][1].append(activity)
  await session.flush()
  for activity_to_hide in activities_to_hide:
    hidden_activity = HiddenActivity(
      activity_id=activity_to_hide.id, user_id=user_id
    )
    session.add(hidden_activity)
  await session.flush()
  return categories_with_activities
