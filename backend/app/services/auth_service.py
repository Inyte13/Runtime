from datetime import datetime, timedelta, timezone

from app.core.constants import GRACE_PERIOD_DAYS
from app.core.exceptions.account_exception import (
  AccountActiveError,
  AccountDeleteError,
  AccountInactiveError,
  AccountRecoverableError,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.services.access_token_service import access_token_service
from app.services.refresh_token_service import refresh_token_service
from app.services.user_service import user_service
from app.utils.google import verificar_google_token
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
  def __init__(self):
    self.user_service = user_service
    self.refresh_token_service = refresh_token_service

  async def login(self, session: AsyncSession, credential: str) -> User:
    google_user_data = await verificar_google_token(credential)
    user_bd = await user_repository.get_by_google(
      session, google_user_data.google_id
    )
    if user_bd is None:
      user_bd = await self.user_service.create(session, google_user_data)
    if user_bd.is_active:
      return user_bd

    assert user_bd.deactivated_at is not None

    if user_bd.deactivated_at.tzinfo is None:
      # Postgres almacena este valor en UTC
      user_bd.deactivated_at = user_bd.deactivated_at.replace(
        tzinfo=timezone.utc
      )
    if datetime.now(timezone.utc) >= (
      user_bd.deactivated_at + timedelta(days=GRACE_PERIOD_DAYS)
    ):
      await user_repository.delete(session, user_bd)
      # commit porque nuestro get_session() hace rollback por cada exception
      await session.commit()
      raise AccountDeleteError()
    raise AccountRecoverableError()

  async def refresh(
    self, session: AsyncSession, refresh_token_id: str
  ) -> tuple[str, RefreshToken]:
    refresh_token = await self.refresh_token_service.get(
      session, refresh_token_id
    )
    user_bd = await self.user_service.get(session, refresh_token.user_id)
    if user_bd.is_active is False:
      raise AccountInactiveError()

    await self.refresh_token_service.delete(session, refresh_token_id)
    new_refresh_token = await self.refresh_token_service.create(
      session, user_bd.id
    )
    new_access_token = access_token_service.create({'id': str(user_bd.id)})
    return new_access_token, new_refresh_token

  async def reactivate(self, session: AsyncSession, credential: str) -> User:
    google_user_data = await verificar_google_token(credential)
    user_bd = await self.user_service.get_by_google(
      session, google_user_data.google_id
    )
    if user_bd.is_active:
      raise AccountActiveError()
    assert user_bd.deactivated_at is not None
    if user_bd.deactivated_at.tzinfo is None:
      # Postgres almacena este valor en UTC
      user_bd.deactivated_at = user_bd.deactivated_at.replace(
        tzinfo=timezone.utc
      )
    if datetime.now(timezone.utc) >= (
      user_bd.deactivated_at + timedelta(days=GRACE_PERIOD_DAYS)
    ):
      await user_repository.delete(session, user_bd)
      # commit porque nuestro get_session() hace rollback por cada exception
      await session.commit()
      raise AccountDeleteError()
    user_bd.is_active = True
    user_bd.deactivated_at = None
    return user_bd

  async def logout(
    self, session: AsyncSession, refresh_token_id: str | None
  ) -> None:
    if refresh_token_id:
      await self.refresh_token_service.delete(session, refresh_token_id)


auth_service = AuthService()
