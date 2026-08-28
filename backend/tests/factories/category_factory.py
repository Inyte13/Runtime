import uuid

from app.core.constants import DEFAULT_CATEGORY_COLOR
from app.models.activity import Activity
from app.models.category import Category
from pydantic_extra_types import Color
from sqlalchemy.ext.asyncio import AsyncSession


async def create_categories(
  session: AsyncSession,
  user_id: uuid.UUID,
  count: int = 2,
  activities_per_category: int = 1,
  overrides_activities_per_category: dict[int, int] | None = None,
) -> list[Category]:

  overrides_activities_per_category = (
    {}
    if overrides_activities_per_category is None
    else overrides_activities_per_category
  )
  categories: list[Category] = []

  for category_index in range(1, count + 1):
    category = Category(
      user_id=user_id,
      name=f'Categoria {category_index}',
      color=Color(DEFAULT_CATEGORY_COLOR),
    )
    session.add(category)
    await session.flush()

    activities_count = overrides_activities_per_category.get(
      category_index,
      activities_per_category,
    )
    for activity_index in range(1, activities_count + 1):
      activity = Activity(
        user_id=user_id,
        category_id=category.id,
        name=f'Actividad {category_index}.{activity_index}',
      )
      session.add(activity)
    categories.append(category)

  await session.flush()
  return categories
