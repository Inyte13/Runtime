import uuid
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import override

from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserUpdate]):
  @override
  async def create(  # type: ignore
    self, session: AsyncSession, user: User
  ) -> User:
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user

  @override
  async def get(  # type: ignore
    self, session: AsyncSession, id: uuid.UUID
  ) -> User | None:
    return await session.get(User, id)

  async def get_all(self, session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

  async def get_by_google(
    self, session: AsyncSession, google_id: str
  ) -> User | None:
    statement = select(User).where(User.google_id == google_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

  async def deactivate(self, session: AsyncSession, user: User) -> User:
    user.is_active = False
    user.deactivated_at = datetime.now(timezone.utc)
    await session.flush()
    return user


user_repository = UserRepository(User)
