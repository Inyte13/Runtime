import uuid

from app.models.hidden_activity import HiddenActivity
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActividadOcultaRepository:
  async def create(
    self, session: AsyncSession, user_id: uuid.UUID, activity_id: uuid.UUID
  ) -> HiddenActivity:
    actividad_oculta = HiddenActivity(user_id=user_id, activity_id=activity_id)
    session.add(actividad_oculta)
    await session.flush()
    return actividad_oculta

  async def delete(
    self, session: AsyncSession, user_id: uuid.UUID, activity_id: uuid.UUID
  ) -> bool:
    statement = (
      select(HiddenActivity)
      .where(HiddenActivity.user_id == user_id)
      .where(HiddenActivity.activity_id == activity_id)
    )
    result = await session.execute(statement)
    actividad_oculta = result.scalar_one_or_none()
    if actividad_oculta:
      await session.delete(actividad_oculta)
      return True
    return False


actividad_oculta_repository = ActividadOcultaRepository()
