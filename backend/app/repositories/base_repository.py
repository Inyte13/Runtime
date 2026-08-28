import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar('Model')
ModelCreate = TypeVar('ModelCreate', bound=BaseModel)
ModelUpdate = TypeVar('ModelUpdate', bound=BaseModel)


class BaseRepository(Generic[Model, ModelUpdate]):
  """Base repository para el CRUD de nuetros repositories"""

  def __init__(self, model: type[Model]):
    self.model = model

  async def create(self, session: AsyncSession, model: Model) -> Model:
    session.add(model)
    await session.flush()
    return model

  async def get(
    self, session: AsyncSession, id: uuid.UUID, user_id: uuid.UUID
  ) -> Model | None:
    statement = (
      select(self.model)
      .where(getattr(self.model, 'id') == id)
      .where(getattr(self.model, 'user_id') == user_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

  async def update(
    self, session: AsyncSession, modelo_obj: Model, model: ModelUpdate
  ) -> Model:
    update_data = model.model_dump(exclude_unset=True)
    # Parseamos de dict directamente update los campos
    for field, value in update_data.items():
      # SQLAlchemy compara el valor con el nuevo, solo manda si hay cambios
      setattr(modelo_obj, field, value)
    await session.flush()
    return modelo_obj

  async def delete(self, session: AsyncSession, modelo_obj: Model) -> None:
    await session.delete(modelo_obj)
