import uuid
from typing import Any, TypeVar

from app.core.exceptions.generic_exception import NotFoundError
from app.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


async def get_or_raise(
  session: AsyncSession,
  repository: BaseRepository[T, Any],
  id: uuid.UUID,
  user_id: uuid.UUID,
) -> T:
  result = await repository.get(session, id, user_id)
  if result is None:
    raise NotFoundError(f'{repository.model.__name__} no se encontró')
  return result
