import uuid
from typing import Sequence

from app.models.actividad import Actividad
from app.models.categoria import Categoria
from app.repositories.base_respository import BaseRepository
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoriaRepository(
  BaseRepository[Categoria, CategoriaCreate, CategoriaUpdate]
):
  async def is_exist_actividad(
    self, session: AsyncSession, id: uuid.UUID
  ) -> bool:
    subquery = select(Actividad.id).where(Actividad.id_categoria == id).exists()
    result = await session.execute(select(subquery))
    # scalars: extrae el primer elemento de cada tupla
    return bool(result.scalar())

  async def get_all(
    self, session: AsyncSession, id_usuario: uuid.UUID
  ) -> Sequence[Categoria]:
    statement = (
      select(Categoria)
      .where(Categoria.id_usuario == id_usuario)
      .order_by(Categoria.nombre)
    )
    result = await session.execute(statement)
    return result.scalars().all()

categoria_repository = CategoriaRepository(Categoria)
