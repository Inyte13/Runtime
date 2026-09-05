import uuid

from app.core.exceptions.generic_exception import NotFoundError
from app.models.hidden_activity import HiddenActivity
from app.repositories.activity_repository import activity_repository
from app.repositories.hidden_activity_repository import (
  hidden_activity_repository,
)
from app.schemas.hidden_activity_schema import HiddenActivityCreate
from app.services.base_service import get_or_raise
from sqlalchemy.ext.asyncio import AsyncSession


class HiddenActivityService:
  def __init__(self):
    self.repository = hidden_activity_repository

  async def create(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    hidden_activity_create: HiddenActivityCreate,
  ) -> HiddenActivity:
    await get_or_raise(
      session, activity_repository, hidden_activity_create.activity_id, user_id
    )
    new_hidden_activity = HiddenActivity(
      activity_id=hidden_activity_create.activity_id,
      user_id=user_id,
    )
    return await self.repository.create(session, new_hidden_activity)

  async def delete(
    self, session: AsyncSession, activity_id: uuid.UUID, user_id: uuid.UUID
  ) -> None:
    await get_or_raise(session, activity_repository, activity_id, user_id)
    hidden_activity_bd = await self.repository.get(
      session, activity_id, user_id
    )
    if hidden_activity_bd is None:
      raise NotFoundError('HiddenActivity no se encontró')
    await self.repository.delete(session, hidden_activity_bd)


hidden_activity_service = HiddenActivityService()
