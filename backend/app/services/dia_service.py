import uuid
from collections.abc import Sequence
from datetime import date, datetime, time, timedelta

from app.core.exceptions.generic import (
  ConflictError,
  InvalidDateRangeError,
  NotFoundError,
)
from app.models.bloque import Bloque
from app.models.dia import Dia
from app.repositories.bloque_repository import bloque_repository
from app.repositories.dia_repository import dia_repository
from app.schemas.actividad import ActividadResumen
from app.schemas.categoria import CategoriaResumen
from app.schemas.dia import DiaResumen, DiaUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class DiaService:
  def __init__(self):
    self.repository = dia_repository

  async def buscar_detail(
    self, session: AsyncSession, id_usuario: uuid.UUID, fecha: date
  ) -> Dia:
    dia = await self.repository.get_detail(session, fecha, id_usuario)
    if not dia:
      raise NotFoundError('Día no encontrado')
    return dia

  async def mostrar_resumen(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    inicio: date,
    final: date,
  ) -> Sequence[Dia]:
    if final < inicio:
      raise InvalidDateRangeError(
        'La fecha final debe ser mayor que la inicial'
      )
    # Si quieres buscar un día mejor hazlo con buscar_dia
    if final == inicio:
      raise InvalidDateRangeError('Las fechas no pueden ser iguales')
    # Solo se puede mostrar máximo 1 año
    if (final - inicio).days > 365:
      raise InvalidDateRangeError('El intervalo no puede ser mayor a 1 año')
    return await self.repository.get_resumen_by_range(
      session, inicio, final, id_usuario
    )

  async def resumen(
    self, session: AsyncSession, id_usuario: uuid.UUID, dia: Dia
  ) -> DiaResumen:
    bloques_resumen = await self.repository.get_bloques_resumen(
      session, dia.fecha, id_usuario
    )
    categorias: dict[uuid.UUID, CategoriaResumen] = {}
    actividades: dict[uuid.UUID, ActividadResumen] = {}
    for id_actividad, duracion, descripcion, id_categoria in bloques_resumen:
      if id_categoria not in categorias:
        categorias[id_categoria] = CategoriaResumen(
          id=id_categoria, actividades=[]
        )
      if id_actividad not in actividades:
        actividad = ActividadResumen(
          id=id_actividad,
          duracion=duracion,
          descripciones=[descripcion] if descripcion else [],
        )
        actividades[id_actividad] = actividad
        categorias[id_categoria].actividades.append(actividad)
      else:
        actividades[id_actividad].duracion += duracion
        if descripcion:
          actividades[id_actividad].descripciones.append(descripcion)
    # Orden ascendente de las actividades
    for categoria in categorias.values():
      categoria.actividades.sort(key=lambda a: a.duracion, reverse=True)
    return DiaResumen(
      fecha=dia.fecha,
      titulo=dia.titulo,
      categorias=list(categorias.values()),
    )

  async def actualizar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    dia: DiaUpdate,
    fecha: date,
  ) -> Dia:
    dia_bd = await self.repository.get(session, fecha, id_usuario)
    if not dia_bd:
      # Solo usa los campos que se declararon
      datos = dia.model_dump(exclude_unset=True)
      # KWARGS: Granularmente actualiza los campos que sobrevivieron
      new_dia = Dia(fecha=fecha, id_usuario=id_usuario, **datos)
      return await self.repository.create(session, new_dia)
    return await self.repository.update(session, dia_bd, dia)

  async def recalcular_horas(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    fecha: date,
    ids: list[uuid.UUID],
  ) -> list[Bloque]:
    bloques = await bloque_repository.get_by_range(session, fecha, id_usuario)
    # Sacamos los id y lo convertimos a set para comparar con los que nos viene
    if {bloque.id for bloque in bloques} != set(ids):
      raise ConflictError('Los bloques no coinciden')
    # Dict para búsqueda rapida
    bloques_dict = {bloque.id: bloque for bloque in bloques}

    hora_temp = datetime.combine(fecha, time(0, 0))

    bloques_actualizados: list[Bloque] = []
    for id in ids:
      bloque = bloques_dict[id]
      bloque.hora = hora_temp.time()
      # Le sumamos la duracion al temp
      hora_temp += timedelta(hours=bloque.duracion)
      # Le asignamos: hora_fin = hora_temp + duracion
      bloque.hora_fin = hora_temp.time()
      bloques_actualizados.append(bloque)
    return bloques_actualizados

  async def eliminar(
    self, session: AsyncSession, id_usuario: uuid.UUID, fecha: date
  ) -> None:
    dia = await self.repository.get(session, fecha, id_usuario)
    if not dia:
      raise NotFoundError('Dia not found')
    return await self.repository.delete(session, dia)


dia_service = DiaService()
