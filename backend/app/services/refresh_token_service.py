import uuid
from datetime import datetime, timezone

from app.core.exceptions.generic import NotFoundError
from app.core.exceptions.token import (
  ExpiredRefreshTokenError,
  MalformedRefreshTokenError,
)
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import refresh_token_repository
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshTokenService:
  def __init__(self):
    self.repository = refresh_token_repository

  async def registrar(
    self, session: AsyncSession, id_usuario: uuid.UUID
  ) -> RefreshToken:
    return await self.repository.create(session, id_usuario)

  async def buscar(self, session: AsyncSession, id: str) -> RefreshToken:
    try:
      id_uuid = uuid.UUID(id)
    # Porque el de arriba tira ValueError
    except ValueError:
      raise MalformedRefreshTokenError()
    refresh_token = await self.repository.get(session, id_uuid)
    if not refresh_token:
      raise NotFoundError('RefreshToken not found')
    expires_at = refresh_token.expires_at
    # Si no tiene UTC, le inyectamos
    if expires_at.tzinfo is None:
      expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
      raise ExpiredRefreshTokenError()

    return refresh_token

  async def eliminar(self, session: AsyncSession, id: str) -> None:
    refresh_token = await self.buscar(session, id)
    await self.repository.delete(session, refresh_token)


refresh_token_service = RefreshTokenService()
