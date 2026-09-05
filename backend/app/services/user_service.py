import uuid

from app.core.constants import (
  DEFAULT_ACTIVITY_NAME,
  DEFAULT_CATEGORY_COLOR,
  DEFAULT_CATEGORY_NAME,
)
from app.core.exceptions.generic_exception import NotFoundError
from app.models.activity import Activity
from app.models.category import Category
from app.models.user import User
from app.repositories.activity_repository import activity_repository
from app.repositories.category_repository import category_repository
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import UserUpdate
from app.services.base_service import get_or_raise
from app.utils.google import GoogleUserData
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
  def __init__(self):
    self.repository = user_repository

  async def get(self, session: AsyncSession, id: uuid.UUID) -> User:
    user = await self.repository.get(session, id)
    if user is None:
      raise NotFoundError()
    return user

  async def get_by_google(self, session: AsyncSession, google_id: str) -> User:
    user = await user_repository.get_by_google(session, google_id)
    if user is None:
      raise NotFoundError()
    return user

  async def create(
    self, session: AsyncSession, google_user_data: GoogleUserData
  ) -> User:
    new_user = User(
      google_id=google_user_data.google_id,
      email=google_user_data.email,
      email_verified=google_user_data.email_verified,
      given_name=google_user_data.given_name,
      family_name=google_user_data.family_name,
      picture_url=google_user_data.picture_url,
      default_activity_id=None,
    )
    user_bd = await self.repository.create(session, new_user)

    default_category = Category(
      name=DEFAULT_CATEGORY_NAME,
      color=DEFAULT_CATEGORY_COLOR,
      user_id=user_bd.id,
    )
    category_bd = await category_repository.create(session, default_category)

    default_activity = Activity(
      name=DEFAULT_ACTIVITY_NAME,
      category_id=category_bd.id,
      user_id=user_bd.id,
    )
    activity_bd = await activity_repository.create(session, default_activity)
    user_bd.default_activity_id = activity_bd.id
    await session.flush()  # Para flushear su activity default
    return user_bd

  async def update(
    self,
    session: AsyncSession,
    user: User,
    user_update: UserUpdate,
  ) -> User:
    await get_or_raise(
      session,
      activity_repository,
      user_update.default_activity_id,
      user.id,
    )
    return await self.repository.update(session, user, user_update)

  async def delete(self, session: AsyncSession, id: uuid.UUID) -> None:
    user_update = await self.get(session, id)
    await self.repository.delete(session, user_update)


user_service = UserService()
