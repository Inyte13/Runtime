import uuid

from app.core.exceptions.activity_exception import DefaultActivityMissingError
from app.core.exceptions.category_exception import DefaultCategoryDeletionError
from app.core.exceptions.generic_exception import ConflictError
from app.models.activity import Activity
from app.models.category import Category
from app.models.user import User
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
    self, session: AsyncSession, user: User
  ) -> list[CategoryResponseDetail]:
    categories_bd = await self.repository.get_all(session, user.id)
    activities_bd = await activity_repository.get_all(session, user.id)

    categories_with_activities: dict[uuid.UUID, list[Activity]] = {}
    activities_ids: list[uuid.UUID] = []
    for activity_bd in activities_bd:
      activities_ids.append(activity_bd.id)
      category_id = activity_bd.category_id
      if category_id not in categories_with_activities:
        categories_with_activities[category_id] = []
      categories_with_activities[category_id].append(activity_bd)

    is_deletable_map = await activity_repository.get_is_deletable_map(
      session, activities_ids
    )

    category_result: list[CategoryResponseDetail] = []
    for category_bd in categories_bd:
      activities_result: list[ActivityResponseDetail] = []
      category_is_deletable = True
      activities = categories_with_activities.get(category_bd.id, [])
      for activity in activities:
        activity_is_deletable = is_deletable_map.get(activity.id, True)
        if activity.id == user.default_activity_id:
          activity_is_deletable = False
        if not activity_is_deletable:
          category_is_deletable = False
        activities_result.append(
          ActivityResponseDetail(
            id=activity.id,
            name=activity.name,
            deletable=activity_is_deletable,
          )
        )
      category_result.append(
        CategoryResponseDetail(
          id=category_bd.id,
          name=category_bd.name,
          color=category_bd.color,
          activities=activities_result,
          deletable=category_is_deletable,
        )
      )
    return category_result

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
    user: User,
    id: uuid.UUID,
  ) -> None:
    category_bd = await get_or_raise(session, self.repository, id, user.id)
    if user.default_activity_id is None:
      raise DefaultActivityMissingError('User no tiene default activity')
    default_activity = await get_or_raise(
      session, activity_repository, user.default_activity_id, user.id
    )
    if default_activity.category_id == id:
      raise DefaultCategoryDeletionError()
    if not await self.repository.is_deletable(session, id):
      raise ConflictError(
        'No se puede eliminar una category con activities que estén usándose'
      )
    await self.repository.delete(session, category_bd)


category_service = CategoryService()
