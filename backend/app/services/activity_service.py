import uuid

from app.core.exceptions.activity_exception import DefaultActivityDeletionError
from app.core.exceptions.generic_exception import ConflictError
from app.models.activity import Activity
from app.models.user import User
from app.repositories.activity_repository import activity_repository
from app.repositories.category_repository import category_repository
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate
from app.services.base_service import get_or_raise
from sqlalchemy.ext.asyncio import AsyncSession


class ActivityService:
  def __init__(self):
    self.repository = activity_repository

  async def create(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    activity_create: ActivityCreate,
  ) -> Activity:
    await get_or_raise(
      session, category_repository, activity_create.category_id, user_id
    )
    new_activity = Activity(
      name=activity_create.name,
      category_id=activity_create.category_id,
      user_id=user_id,
    )
    return await self.repository.create(session, new_activity)

  async def update(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    activity_update: ActivityUpdate,
    id: uuid.UUID,
  ) -> Activity:
    activity_bd = await get_or_raise(session, self.repository, id, user_id)
    if activity_update.category_id is not None:
      await get_or_raise(
        session, category_repository, activity_update.category_id, user_id
      )
    return await self.repository.update(session, activity_bd, activity_update)

  async def delete(
    self,
    session: AsyncSession,
    user: User,
    id: uuid.UUID,
  ) -> None:
    activity_bd = await get_or_raise(session, self.repository, id, user.id)
    if user.default_activity_id == id:
      raise DefaultActivityDeletionError()
    if not await self.repository.is_deletable(session, id):
      raise ConflictError(
        'No se puede delete una activity con al menos un bloque relacionado'
      )
    await self.repository.delete(session, activity_bd)


activity_service = ActivityService()
