import uuid
from typing import Sequence

from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.repositories.base_respository import BaseRepository
from app.schemas.actividad import ActividadCreate, ActividadUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActividadRepository(
  BaseRepository[Actividad, ActividadCreate, ActividadUpdate]
):
  async def get_multi(
    self, session: AsyncSession, skip: int = 0, limit: int = 100
  ) -> Sequence[Actividad]:
    raise NotImplementedError('El get_multi no está definido en Actividad')

  async def is_exist_bloque(self, session: AsyncSession, id: uuid.UUID) -> bool:
    subquery = select(Bloque.id).where(Bloque.id_actividad == id).exists()
    result = await session.execute(select(subquery))
    # scalars: extrae el primer elemento de cada tupla
    return bool(result.scalar())


actividad_repository = ActividadRepository(Actividad)
