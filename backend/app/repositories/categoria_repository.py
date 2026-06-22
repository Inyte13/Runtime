import uuid
from collections.abc import Sequence

from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.models.categoria import Categoria
from app.repositories.base_respository import BaseRepository
from app.schemas.categoria import CategoriaUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CategoriaRepository(BaseRepository[Categoria, CategoriaUpdate]):
  async def tiene_actividad_with_bloque(
    self, session: AsyncSession, id: uuid.UUID
  ) -> bool:
    statement = (
      select(Actividad)
      .join(Bloque, Bloque.id_actividad == Actividad.id)
      .where(Actividad.id_categoria == id)
      .limit(1)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None

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

  # get_all pero precarga las actividades para añadirle tiene_bloques, necesita estar precargado
  async def get_all_with_actividades(
    self, session: AsyncSession, id_usuario: uuid.UUID
  ) -> Sequence[Categoria]:
    statement = (
      select(Categoria)
      .where(Categoria.id_usuario == id_usuario)
      .order_by(Categoria.nombre)
      .options(selectinload(Categoria.actividades))
    )
    result = await session.execute(statement)
    return result.scalars().all()


categoria_repository = CategoriaRepository(Categoria)
