import uuid

from app.models.actividad_oculta import ActividadOculta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActividadOcultaRepository:
  async def create(
    self, session: AsyncSession, id_usuario: uuid.UUID, id_actividad: uuid.UUID
  ) -> ActividadOculta:
    actividad_oculta = ActividadOculta(
      id_usuario=id_usuario, id_actividad=id_actividad
    )
    session.add(actividad_oculta)
    await session.flush()
    return actividad_oculta

  async def delete(
    self, session: AsyncSession, id_usuario: uuid.UUID, id_actividad: uuid.UUID
  ) -> bool:
    statement = (
      select(ActividadOculta)
      .where(ActividadOculta.id_usuario == id_usuario)
      .where(ActividadOculta.id_actividad == id_actividad)
    )
    result = await session.execute(statement)
    actividad_oculta = result.scalar_one_or_none()
    if actividad_oculta:
      await session.delete(actividad_oculta)
      return True
    return False
