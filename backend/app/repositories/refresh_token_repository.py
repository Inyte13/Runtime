import uuid
from datetime import datetime, timedelta, timezone

from app.core.settings import get_settings
from app.models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshTokenRepository:
  async def create(
    self, session: AsyncSession, user_id: uuid.UUID
  ) -> RefreshToken:
    expires_at = datetime.now(timezone.utc) + timedelta(
      days=get_settings().REFRESH_TOKEN_DURATION_DAYS
    )
    refresh_token = RefreshToken(user_id=user_id, expires_at=expires_at)
    session.add(refresh_token)
    await session.flush()
    return refresh_token

  async def get(
    self, session: AsyncSession, id: uuid.UUID
  ) -> RefreshToken | None:
    return await session.get(RefreshToken, id)

  async def delete(
    self, session: AsyncSession, refresh_token: RefreshToken
  ) -> None:
    await session.delete(refresh_token)


refresh_token_repository = RefreshTokenRepository()
