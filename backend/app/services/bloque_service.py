from datetime import date, datetime, time, timedelta
from typing import Sequence

from sqlmodel import Session, desc, select

from app.crud.bloque_crud import (
  create_bloque,
  delete_bloque,
  read_bloque,
  read_bloques_by_range,
  update_bloque,
)
from app.crud.dia_crud import create_dia, read_dia
from app.models.bloque import Bloque
from app.models.dia import Dia
from app.schemas.bloque_schema import BloqueCreate, BloqueUpdate
from app.services.actividad_service import buscar_actividad


def _ultimo_bloque(session: Session, fecha) -> Bloque | None:
  statement = (
    select(Bloque).where(Bloque.fecha == fecha).order_by(desc(Bloque.hora))
  )
  return session.exec(statement).first()


def _modificar_hora(hora: time, duracion: float) -> time:
  inicio = datetime.combine(date.today(), hora)
  fin = inicio + timedelta(hours=duracion)
  return fin.time()


def _modificar_horas(
  session: Session, bloques: Sequence[Bloque], diferencia: float
) -> None:
  for bloque in bloques:
    bloque.hora = _modificar_hora(bloque.hora, diferencia)
    if bloque.duracion is not None:
      bloque.hora_fin = _modificar_hora(bloque.hora, bloque.duracion)
    session.add(bloque)


def _validar_actividad(session: Session, id: int) -> None:
  actividad = buscar_actividad(session, id)
  if not actividad.is_active:
    raise ValueError('La actividad está archivada')


def _validar_hora_granulidad(hora: time, unidad_duracion: int = 30) -> None:
  if (
    hora.minute % unidad_duracion != 0
    or hora.second != 0
    or hora.microsecond != 0
  ):
    raise ValueError(
      f'La hora debe estar en múltiplos de {unidad_duracion} minutos'
    )


def buscar_bloque(session: Session, id: int) -> Bloque:
  bloque = read_bloque(session, id)
  if not bloque:
    raise ValueError('No se encontró el bloque')
  return bloque


def registrar_bloque(session: Session, bloque: BloqueCreate) -> Bloque:
  # Patrón Get or Create
  # No usamos buscar_dia para controlar cuando no existe
  dia = read_dia(session, bloque.fecha)
  if not dia:
    dia = create_dia(session, Dia(fecha=bloque.fecha))

  # El último bloque del día
  ultimo = _ultimo_bloque(session, fecha)

  # Si el usuario manda
  id_actividad = bloque.id_actividad

  # Si es el primer bloque
  if not ultimo:
    # Le ponemos hora 00:00
    hora = time(0, 0)
    if id_actividad is None:
      # Actividad 'Dormir'
      id_actividad = 1
  else:
    # Si el ultimo bloque no tiene una hora_fin declarado 400
    if ultimo.hora_fin is None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='No se puede crear un bloque sin antes definir la duración del anterior',
      )
    # Si lo tiene lo asignamos como hora al bloque creado
    hora = ultimo.hora_fin
    if id_actividad is None:
      # Actividad 'Empty'
      id_actividad = 2

  _validar_actividad(session, id_actividad)
  _validar_hora_granulidad(hora, unidad_bloque=30)

  new_bloque = Bloque(
    hora=hora,
    descripcion=bloque.descripcion,
    id_actividad=id_actividad,
    fecha=fecha,
    duracion=bloque.duracion,
  )
  bloque_bd = create_bloque(session, new_bloque)
  return bloque_bd


def actualizar_bloque(
  session: Session, id: int, bloque: BloqueUpdate
) -> Bloque:
  bloque_bd = buscar_bloque(session, id)
  if bloque.id_actividad:
    # Validamos la actividad ingresada
    _validar_actividad(session, bloque.id_actividad)

  # Siempre que tenga duracion y no sea la misma
  if bloque.duracion is not None and bloque.duracion != bloque_bd.duracion:
    # Por en la bd la duracion es null
    duracion = bloque_bd.duracion or 0.0
    # El delta que tendra que cambiar en los bloques siguientes
    diferencia = bloque.duracion - duracion

    # Actualizamos la duracion
    bloque_bd.duracion = bloque.duracion
    # Actualizamos la hora_fin
    bloque_bd.hora_fin = _modificar_hora(bloque_bd.hora, bloque.duracion)

    # Traemos los siguientes
    bloques_siguientes = read_bloques_by_range(
      session=session,
      fecha=bloque_bd.fecha,
      hora_desde=bloque_bd.hora,
      incluir_desde=False,  # Sin incluir el actual
    )
    # modificamos la duracion de todos los siguientes
    _modificar_horas(session, bloques_siguientes, diferencia)

  bloque_bd = update_bloque(session, bloque_bd, bloque)
  return bloque_bd


def eliminar_bloque(session: Session, id: int) -> None:
  bloque = buscar_bloque(session, id)
  if bloque.duracion is not None:
    diferencia = -bloque.duracion
    bloques_siguientes = read_bloques_by_range(
      session=session,
      fecha=bloque.fecha,
      hora_desde=bloque.hora,
      incluir_desde=False,
    )
    _modificar_horas(session, bloques_siguientes, diferencia)
  delete_bloque(session, bloque)
