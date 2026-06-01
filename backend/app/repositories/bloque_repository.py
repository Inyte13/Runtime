import uuid
from datetime import date, time
from typing import Sequence

from app.models.bloque import Bloque
from app.repositories.base_respository import BaseRepository
from app.schemas.bloque import BloqueCreate, BloqueUpdate
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class BloqueRepository(BaseRepository[Bloque, BloqueCreate, BloqueUpdate]):
  async def ultimo(
    self, session: AsyncSession, fecha: date, id_usuario: uuid.UUID
  ) -> Bloque | None:
    statement = (
      select(Bloque)
      .where(Bloque.fecha == fecha, Bloque.id_usuario == id_usuario)
      .order_by(desc(Bloque.hora))
    )
    result = await session.execute(statement)
    # scalars: extrae el primer elemento de cada tupla
    return result.scalars().first()

  async def get_by_range(
    self,
    session: AsyncSession,
    fecha: date,
    id_usuario: uuid.UUID,
    hora_desde: time | None = None,
    hora_hasta: time | None = None,
  ) -> Sequence[Bloque]:
    statement = (
      select(Bloque)
      .where(Bloque.fecha == fecha, Bloque.id_usuario == id_usuario)
      .order_by(Bloque.hora)
    )
    if hora_desde is not None:
      statement = statement.where(Bloque.hora >= hora_desde)
    if hora_hasta is not None:
      statement = statement.where(Bloque.hora <= hora_hasta)
    result = await session.execute(statement)
    # scalars: extrae el primer elemento de cada tupla
    return result.scalars().all()


bloque_repository = BloqueRepository(Bloque)
