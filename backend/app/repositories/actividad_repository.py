import uuid

from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.repositories.base_respository import BaseRepository
from app.schemas.actividad import ActividadUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActividadRepository(BaseRepository[Actividad, ActividadUpdate]):
  async def tiene_bloque(self, session: AsyncSession, id: uuid.UUID) -> bool:
    subquery = select(Bloque.id).where(Bloque.id_actividad == id).exists()
    result = await session.execute(select(subquery))
    return bool(result.scalar())

  async def get_tiene_bloque_map(
    self, session: AsyncSession, ids_actividades: list[uuid.UUID]
  ) -> dict[uuid.UUID, bool]:
    if not ids_actividades:
      return {}
    statement = (
      select(Bloque.id_actividad)
      .where(Bloque.id_actividad.in_(ids_actividades))
      .distinct()
    )
    result = await session.execute(statement)
    # Solo guardamos True, porque cuando lo usemos indicaremos default False
    return {id_actividad: True for id_actividad in result.scalars().all()}


actividad_repository = ActividadRepository(Actividad)
