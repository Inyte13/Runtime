import uuid

from app.core.exceptions.generic import ConflictError
from app.models.actividad import Actividad
from app.repositories.actividad_repository import actividad_repository
from app.repositories.categoria_repository import categoria_repository
from app.schemas.actividad import ActividadCreate, ActividadUpdate
from app.services.base import get_or_raise
from sqlalchemy.ext.asyncio import AsyncSession


class ActividadService:
  def __init__(self):
    self.repository = actividad_repository

  async def registrar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    actividad: ActividadCreate,
  ) -> Actividad:
    # Valido si la id_categoria existe para el usuario
    await get_or_raise(
      session, categoria_repository, actividad.id_categoria, id_usuario
    )
    new_actividad = Actividad(
      nombre=actividad.nombre,
      id_categoria=actividad.id_categoria,
      id_usuario=id_usuario,
    )
    # En lugar de ponerle eliminable en true, lo hacemos en schemas porque el refrescar ignora variables temporales
    return await self.repository.create(session, new_actividad)

  async def actualizar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    actividad: ActividadUpdate,
    id: uuid.UUID,
  ) -> Actividad:
    actividad_bd = await get_or_raise(session, self.repository, id, id_usuario)
    # Si quiere cambiar la categoria tengo que validar si es válida para el usuario
    if actividad.id_categoria is not None:
      await get_or_raise(
        session, categoria_repository, actividad.id_categoria, id_usuario
      )
    return await self.repository.update(session, actividad_bd, actividad)

  async def eliminar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    id: uuid.UUID,
  ) -> None:
    actividad = await get_or_raise(session, self.repository, id, id_usuario)
    if await self.repository.tiene_bloque(session, id):
      raise ConflictError(
        'No se puede eliminar una actividad con al menos un bloque relacionado'
      )
    await self.repository.delete(session, actividad)


actividad_service = ActividadService()
