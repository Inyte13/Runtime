import uuid

from app.core.exceptions.generic import ConflictError
from app.models.categoria import Categoria
from app.repositories.actividad_repository import actividad_repository
from app.repositories.categoria_repository import categoria_repository
from app.schemas.actividad import ActividadResponseDetail
from app.schemas.categoria import (
  CategoriaCreate,
  CategoriaResponseDetail,
  CategoriaUpdate,
)
from app.services.base import get_or_raise
from sqlalchemy.ext.asyncio import AsyncSession


class CategoriaService:
  def __init__(self):
    self.repository = categoria_repository

  async def registrar(
    self,
    session: AsyncSession,
    categoria: CategoriaCreate,
    id_usuario: uuid.UUID,
  ) -> Categoria:
    new_categoria = Categoria(
      nombre=categoria.nombre, color=categoria.color, id_usuario=id_usuario
    )
    return await self.repository.create(session, new_categoria)

  async def mostrar_todas(
    self, session: AsyncSession, id_usuario: uuid.UUID
  ) -> list[CategoriaResponseDetail]:
    categorias = await self.repository.get_all_with_actividades(
      session, id_usuario
    )

    ids_actividades: list[uuid.UUID] = []
    for categoria in categorias:
      for actividad in categoria.actividades:
        ids_actividades.append(actividad.id)

    tiene_bloque_map = await actividad_repository.get_tiene_bloque_map(
      session, ids_actividades
    )

    result: list[CategoriaResponseDetail] = []
    for categoria in categorias:
      actividades: list[ActividadResponseDetail] = []
      tiene_actividad_con_bloque = False
      for actividad in categoria.actividades:
        tiene_bloques = tiene_bloque_map.get(actividad.id, False)
        if tiene_bloques:
          tiene_actividad_con_bloque = True
        actividades.append(
          ActividadResponseDetail(
            id=actividad.id,
            nombre=actividad.nombre,
            eliminable= not tiene_bloques,
          )
        )
      result.append(
        CategoriaResponseDetail(
          id=categoria.id,
          nombre=categoria.nombre,
          color=categoria.color,
          actividades=actividades,
          eliminable=not tiene_actividad_con_bloque,
        )
      )
    return result

  async def actualizar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    categoria: CategoriaUpdate,
    id: uuid.UUID,
  ) -> Categoria:
    categoria_bd = await get_or_raise(session, self.repository, id, id_usuario)
    return await self.repository.update(session, categoria_bd, categoria)

  async def eliminar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    id: uuid.UUID,
  ) -> None:
    categoria = await get_or_raise(session, self.repository, id, id_usuario)
    if await self.repository.tiene_actividad_with_bloque(session, id):
      raise ConflictError(
        'No se puede eliminar una categoría con actividades que tengan bloques'
      )
    await self.repository.delete(session, categoria)


categoria_service = CategoriaService()
