import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Modelo = TypeVar('Modelo')
ModeloCreate = TypeVar('ModeloCreate', bound=BaseModel)
ModeloUpdate = TypeVar('ModeloUpdate', bound=BaseModel)


# En los params tenemos:
# Modelo SQLAlchemy
# Schemas Pydantic
class BaseRepository(Generic[Modelo, ModeloUpdate]):
  """Base repository para el CRUD de nuetros repositories"""

  def __init__(self, modelo: type[Modelo]):
    self.modelo = modelo

  async def create(self, session: AsyncSession, modelo: Modelo) -> Modelo:
    session.add(modelo)
    await session.flush()
    await session.refresh(modelo)
    return modelo

  async def get(
    self, session: AsyncSession, id: uuid.UUID, id_usuario: uuid.UUID
  ) -> Modelo | None:
    statement = (
      select(self.modelo)
      .where(getattr(self.modelo, 'id') == id)
      .where(getattr(self.modelo, 'id_usuario') == id_usuario)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

  async def update(
    self, session: AsyncSession, modelo_obj: Modelo, modelo: ModeloUpdate
  ) -> Modelo:
    update_data = modelo.model_dump(exclude_unset=True)
    # Parseamos de dict directamente actualizar los campos
    for field, value in update_data.items():
      setattr(modelo_obj, field, value)
    await session.flush()
    await session.refresh(modelo_obj)
    return modelo_obj

  async def delete(self, session: AsyncSession, modelo_obj: Modelo) -> None:
    await session.delete(modelo_obj)
