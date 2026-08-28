import uuid

from app.core.exceptions.generic_exception import ConflictError
from app.models.category import Category
from app.repositories.activity_repository import activity_repository
from app.repositories.category_repository import category_repository
from app.schemas.activity_schema import ActivityResponseDetail
from app.schemas.category_schema import (
  CategoryCreate,
  CategoryResponseDetail,
  CategoryUpdate,
)
from app.services.base_service import get_or_raise
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryService:
  def __init__(self):
    self.repository = category_repository

  async def create(
    self,
    session: AsyncSession,
    category_create: CategoryCreate,
    user_id: uuid.UUID,
  ) -> Category:
    new_category = Category(
      name=category_create.name, color=category_create.color, user_id=user_id
    )
    return await self.repository.create(session, new_category)

  async def get_all_with_activities(
    self, session: AsyncSession, user_id: uuid.UUID
  ) -> list[CategoryResponseDetail]:
    categories_and_activities = await self.repository.get_all_with_activities(
      session, user_id
    )
    activities_ids: list[uuid.UUID] = []
    for category in categories_and_activities:
      for activity in category.activities:
        activities_ids.append(activity.id)

    is_deletable_map = await activity_repository.get_is_deletable_map(
      session, activities_ids
    )

    result: list[CategoryResponseDetail] = []
    for category in categories_and_activities:
      activities: list[ActivityResponseDetail] = []
      category_is_deletable = False
      for activity in category.activities:
        activity_is_deletable = is_deletable_map.get(activity.id, False)
        if activity_is_deletable:
          category_is_deletable = True
        activities.append(
          ActivityResponseDetail(
            id=activity.id,
            name=activity.name,
            deletable=not activity_is_deletable,
          )
        )
      result.append(
        CategoryResponseDetail(
          id=category.id,
          name=category.name,
          color=category.color,
          activities=activities,
          deletable=not category_is_deletable,
        )
      )
    return result

  async def update(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    category_update: CategoryUpdate,
    id: uuid.UUID,
  ) -> Category:
    category_bd = await get_or_raise(session, self.repository, id, user_id)
    return await self.repository.update(session, category_bd, category_update)

  async def delete(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    id: uuid.UUID,
  ) -> None:
    category_bd = await get_or_raise(session, self.repository, id, user_id)
    if not await self.repository.is_deletable(session, id):
      raise ConflictError(
        'No se puede eliminar una categoría con actividades que tengan blocks'
      )
    await self.repository.delete(session, category_bd)


category_service = CategoryService()
