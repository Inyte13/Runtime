from datetime import datetime, timedelta, timezone

from app.core.exceptions.account import (
  AccountActiveError,
  AccountDeleteError,
  AccountInactiveError,
  AccountRecoverableError,
)
from app.core.security import crear_access_token
from app.models.refresh_token import RefreshToken
from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from app.services.refresh_token_service import refresh_token_service
from app.services.usuario_service import usuario_service
from app.utils.google import verificar_google_token
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
  def __init__(self):
    self.usuario_service = usuario_service
    self.refresh_token_service = refresh_token_service

  async def loguear(self, session: AsyncSession, credential: str) -> Usuario:
    data_google = await verificar_google_token(credential)
    usuario_bd = await usuario_repository.get_by_google(
      session, data_google.id_google
    )
    if not usuario_bd:
      usuario_bd = await self.usuario_service.registrar(session, data_google)
    if not usuario_bd.is_active:
      deactivated_at = usuario_bd.deactivated_at
      assert deactivated_at is not None
      # Por si no llega con asyncpg
      # if deactivated_at.tzinfo is None:
      #   deactivated_at = deactivated_at.replace(tzinfo=timezone.utc)
      if datetime.now(timezone.utc) >= (deactivated_at + timedelta(days=30)):
        await usuario_repository.delete(session, usuario_bd)
        raise AccountDeleteError()
      else:
        # No significante, para compararlo y dar 401
        raise AccountRecoverableError()
    return usuario_bd

  async def refrescar(
    self, session: AsyncSession, id_refresh_token: str
  ) -> tuple[str, RefreshToken]:
    refresh_token = await self.refresh_token_service.buscar(
      session, id_refresh_token
    )
    id_usuario = refresh_token.id_usuario
    usuario = await self.usuario_service.buscar(session, id_usuario)
    if not usuario.is_active:
      raise AccountInactiveError()

    await self.refresh_token_service.eliminar(session, id_refresh_token)
    new_refresh_token = await self.refresh_token_service.registrar(
      session, id_usuario
    )
    access_token = crear_access_token({'id': str(id_usuario)})
    return access_token, new_refresh_token

  async def reactivar(self, session: AsyncSession, credential: str) -> Usuario:
    data_google = await verificar_google_token(credential)
    usuario_bd = await self.usuario_service.buscar_by_google(
      session, data_google.id_google
    )
    if usuario_bd.is_active:
      raise AccountActiveError()
    deactivated_at = usuario_bd.deactivated_at
    assert deactivated_at is not None
    if datetime.now(timezone.utc) >= (deactivated_at + timedelta(days=30)):
      await usuario_repository.delete(session, usuario_bd)
      raise AccountDeleteError()
    usuario_bd.is_active = True
    usuario_bd.deactivated_at = None
    await session.flush()
    return usuario_bd

  async def desloguear(
    self, session: AsyncSession, id_refresh_token: str | None
  ) -> None:
    if id_refresh_token:
      await self.refresh_token_service.eliminar(session, id_refresh_token)


auth_service = AuthService()
