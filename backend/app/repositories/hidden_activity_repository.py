import uuid

from app.models.hidden_activity import HiddenActivity
from sqlalchemy.ext.asyncio import AsyncSession


class HiddenActivityRepository:
  async def create(
    self, session: AsyncSession, hidden_activity: HiddenActivity
  ) -> HiddenActivity:
    session.add(hidden_activity)
    await session.flush()
    return hidden_activity

  async def get(
    self, session: AsyncSession, activity_id: uuid.UUID, user_id: uuid.UUID
  ) -> HiddenActivity | None:
    # Solo para pk compuesta
    return await session.get(HiddenActivity, (activity_id, user_id))

  async def delete(
    self, session: AsyncSession, hidden_activity: HiddenActivity
  ) -> None:
    await session.delete(hidden_activity)


hidden_activity_repository = HiddenActivityRepository()
