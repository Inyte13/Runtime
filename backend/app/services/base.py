import uuid
from typing import Any, TypeVar

from app.core.exceptions.generic import NotFoundError
from app.repositories.base_respository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


async def get_or_raise(
  session: AsyncSession,
  repository: BaseRepository[T, Any],
  id: uuid.UUID,
  id_usuario: uuid.UUID,
) -> T:
  result = await repository.get(session, id, id_usuario)
  if not result:
    raise NotFoundError(f'{repository.modelo.__name__} not found')
  return result
