import uuid
from collections.abc import Sequence
from datetime import time

from app.models.bloque import Bloque
from app.models.dia import Dia
from app.models.usuario import Usuario
from app.repositories.actividad_repository import actividad_repository
from app.repositories.bloque_repository import bloque_repository
from app.repositories.dia_repository import dia_repository
from app.schemas.bloque import BloqueCreate, BloqueUpdate
from app.services.base import get_or_raise
from app.utils.time import modificar_hora, validar_hora_granulidad
from sqlalchemy.ext.asyncio import AsyncSession


class BloqueService:
  def __init__(self):
    self.repository = bloque_repository

  def _modificar_horas(
    self, bloques: Sequence[Bloque], diferencia: float
  ) -> None:
    for bloque in bloques:
      bloque.hora = modificar_hora(bloque.hora, diferencia)
      bloque.hora_fin = modificar_hora(bloque.hora, bloque.duracion)

  async def registrar(
    self, session: AsyncSession, usuario: Usuario, bloque: BloqueCreate
  ) -> Bloque:
    # Patrón Get or Create
    dia = await dia_repository.get(session, bloque.fecha, usuario.id)
    if not dia:
      dia = await dia_repository.create(
        session, Dia(fecha=bloque.fecha, id_usuario=usuario.id)
      )
    bloque.id_actividad = usuario.id_actividad_default
    # Para el button de ListaBloques
    if bloque.id_ref is None:
      return await self._registrar_btn(session, bloque, usuario.id)
    # Cuando cree con alt en el primer bloque
    if bloque.id_ref.int == 0:
      # Insertar al inicio
      return await self._registrar_al_inicio(session, bloque, usuario.id)

    # Si existe el id_ref del 'creador'
    return await self._registrar_despues(session, bloque, usuario.id)

  async def _registrar_btn(
    self, session: AsyncSession, bloque: BloqueCreate, id_usuario: uuid.UUID
  ) -> Bloque:
    ultimo = await self.repository.ultimo(session, bloque.fecha, id_usuario)
    # Si es el primer bloque usa el 00:00 sino la hora_fin del ultimo
    if ultimo:
      validar_hora_granulidad(ultimo.hora_fin)
      hora = ultimo.hora_fin
    else:
      hora = time(0, 0)
    new_bloque = Bloque(
      fecha=bloque.fecha,
      duracion=bloque.duracion,
      descripcion=bloque.descripcion,
      hora=hora,
      id_actividad=bloque.id_actividad,
      hora_fin=modificar_hora(hora, bloque.duracion),
      id_usuario=id_usuario,
    )
    return await self.repository.create(session, new_bloque)

  async def _registrar_al_inicio(
    self, session: AsyncSession, bloque: BloqueCreate, id_usuario: uuid.UUID
  ) -> Bloque:
    new_bloque = Bloque(
      fecha=bloque.fecha,
      duracion=bloque.duracion,
      descripcion=bloque.descripcion,
      hora=time(0, 0),
      id_actividad=bloque.id_actividad,
      hora_fin=modificar_hora(time(0, 0), bloque.duracion),
      id_usuario=id_usuario,
    )
    bloque_bd = await self.repository.create(session, new_bloque)
    siguientes = await self.repository.get_by_range(
      session, bloque.fecha, id_usuario, hora_desde=time(0, 0)
    )
    # Cogemos los siguientes pero sin el creado
    siguientes = [b for b in siguientes if b.id != bloque_bd.id]
    self._modificar_horas(siguientes, bloque.duracion)
    return bloque_bd

  async def _registrar_despues(
    self, session: AsyncSession, bloque: BloqueCreate, id_usuario: uuid.UUID
  ) -> Bloque:
    assert bloque.id_ref is not None
    bloque_ref = await get_or_raise(
      session, self.repository, bloque.id_ref, id_usuario
    )
    hora = bloque_ref.hora_fin
    validar_hora_granulidad(hora)
    new_bloque = Bloque(
      fecha=bloque.fecha,
      duracion=bloque.duracion,
      descripcion=bloque.descripcion,
      hora=hora,
      id_actividad=bloque.id_actividad,
      hora_fin=modificar_hora(hora, bloque.duracion),
      id_usuario=id_usuario,
    )
    bloque_bd = await self.repository.create(session, new_bloque)
    # Si lo incluimos porque hora es la hora_fin o sea la hora de inicio de los siguientes
    siguientes = await self.repository.get_by_range(
      session, bloque.fecha, id_usuario, hora_desde=hora
    )
    # Cogemos los siguientes pero sin el creado
    siguientes = [b for b in siguientes if b.id != bloque_bd.id]
    self._modificar_horas(siguientes, new_bloque.duracion)
    return bloque_bd

  async def actualizar(
    self,
    session: AsyncSession,
    id_usuario: uuid.UUID,
    bloque: BloqueUpdate,
    id: uuid.UUID,
  ) -> Bloque:
    bloque_bd = await get_or_raise(session, self.repository, id, id_usuario)
    if bloque.id_actividad:
      await get_or_raise(
        session, actividad_repository, bloque.id_actividad, id_usuario
      )
    # Siempre que tenga duracion y no sea la misma
    if bloque.duracion and bloque.duracion != bloque_bd.duracion:
      # La diferencia que tendrá que cambiar en los bloques siguientes
      diferencia = bloque.duracion - bloque_bd.duracion

      # Actualizamos la duracion
      bloque_bd.duracion = bloque.duracion
      # Actualizamos la hora_fin
      bloque_bd.hora_fin = modificar_hora(bloque_bd.hora, bloque.duracion)

      # Traemos los siguientes
      siguientes = await self.repository.get_by_range(
        session,
        bloque_bd.fecha,
        id_usuario,
        hora_desde=bloque_bd.hora,
      )
      siguientes = [b for b in siguientes if b.id != bloque_bd.id]
      # modificamos la duracion de todos los siguientes
      self._modificar_horas(siguientes, diferencia)

    return await self.repository.update(session, bloque_bd, bloque)

  async def eliminar(
    self, session: AsyncSession, id_usuario: uuid.UUID, id: uuid.UUID
  ) -> None:
    bloque = await get_or_raise(session, self.repository, id, id_usuario)
    ultimo = await self.repository.ultimo(session, bloque.fecha, id_usuario)
    if ultimo and bloque.id != ultimo.id:
      diferencia = -bloque.duracion
      siguientes = await self.repository.get_by_range(
        session, bloque.fecha, id_usuario, hora_desde=bloque.hora
      )
      siguientes = [b for b in siguientes if b.id != bloque.id]
      self._modificar_horas(siguientes, diferencia)
    await self.repository.delete(session, bloque)


bloque_service = BloqueService()
