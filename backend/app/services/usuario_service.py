import uuid

from app.core.constants import (
  ACTIVIDAD_NOMBRE,
  CATEGORIA_COLOR,
  CATEGORIA_NOMBRE,
)
from app.core.exceptions.generic import NotFoundError
from app.models.actividad import Actividad
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.repositories.actividad_repository import actividad_repository
from app.repositories.categoria_repository import categoria_repository
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioUpdate
from app.services.base import get_or_raise
from app.utils.google import DataGoogle
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioService:
  def __init__(self):
    self.repository = usuario_repository

  async def buscar(self, session: AsyncSession, id: uuid.UUID) -> Usuario:
    usuario = await self.repository.get(session, id)
    if not usuario:
      raise NotFoundError('Usuario not found')
    return usuario

  async def buscar_by_google(
    self, session: AsyncSession, id_google: str
  ) -> Usuario:
    usuario = await usuario_repository.get_by_google(session, id_google)
    if not usuario:
      raise NotFoundError('Usuario not found')
    return usuario

  async def registrar(
    self, session: AsyncSession, data_google: DataGoogle
  ) -> Usuario:
    new_usuario = Usuario(
      id_google=data_google.id_google,
      email=data_google.email,
      email_verified=data_google.email_verified,
      given_name=data_google.given_name,
      family_name=data_google.family_name,
      picture_url=data_google.picture_url,
      id_actividad_default=None,
    )
    usuario_bd = await self.repository.create(session, new_usuario)

    categoria_default = Categoria(
      nombre=CATEGORIA_NOMBRE,
      color=CATEGORIA_COLOR,
      id_usuario=usuario_bd.id,
    )
    categoria_bd = await categoria_repository.create(session, categoria_default)

    actividad_default = Actividad(
      nombre=ACTIVIDAD_NOMBRE,
      id_categoria=categoria_bd.id,
      id_usuario=usuario_bd.id,
    )
    actividad_bd = await actividad_repository.create(session, actividad_default)
    usuario_bd.id_actividad_default = actividad_bd.id
    return usuario_bd

  async def actualizar(
    self,
    session: AsyncSession,
    usuario: Usuario,
    usuario_update: UsuarioUpdate,
  ) -> Usuario:
    await get_or_raise(
      session,
      actividad_repository,
      usuario_update.id_actividad_default,
      usuario.id,
    )
    return await self.repository.update(session, usuario, usuario_update)

  async def eliminar(self, session: AsyncSession, id: uuid.UUID) -> None:
    usuario_update = await self.buscar(session, id)
    await self.repository.delete(session, usuario_update)


usuario_service = UsuarioService()
