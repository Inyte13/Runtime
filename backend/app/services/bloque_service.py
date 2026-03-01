from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlmodel import Session, desc, select

from app.crud.actividad_crud import read_actividad_by_id
from app.crud.bloque_crud import (
  create_bloque,
  delete_bloque,
  read_bloque_by_id,
  update_bloque,
)
from app.crud.dia_crud import create_dia, read_dia
from app.models.bloque import Bloque
from app.models.dia import Dia
from app.schemas.bloque_schema import BloqueCreate, BloqueUpdate




def _calcular_hora_fin(
  fecha: date, hora: time, duracion: float | None
) -> time | None:
  if duracion is None:
    return None
  inicio = datetime.combine(fecha, hora)
  fin = inicio + timedelta(hours=duracion)
  return fin.time()


def _validar_actividad(session: Session, id: int) -> None:
  actividad = read_actividad_by_id(session, id)
  if not actividad:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='Actividad no encontrada'
    )
  if not actividad.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='La actividad está en la papelera',
    )
  return


def _validar_hora_granulidad(hora: time, unidad_bloque: int = 30) -> None:
  if (
    hora.minute % unidad_bloque != 0
    or hora.second != 0
    or hora.microsecond != 0
  ):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f'La hora debe estar en múltiplos de {unidad_bloque} minutos',
    )
  return


def buscar_bloque(session: Session, id: int) -> Bloque:
  bloque = read_bloque_by_id(session, id)
  if not bloque:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='Bloque no encontrado'
    )
  return bloque


def registrar_bloque(session: Session, bloque: BloqueCreate) -> Bloque:
  fecha = bloque.fecha or date.today()
  # Primero revisaremos si existe un dia
  dia = read_dia(session, fecha)
  # Si no existe creamos uno
  if not dia:
    dia = create_dia(session, Dia(fecha=fecha))


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

  bloque_bd = update_bloque(session, bloque_bd, bloque)
  return bloque_bd


def eliminar_bloque(session: Session, id: int) -> None:
  bloque = buscar_bloque(session, id)
  delete_bloque(session, bloque)
  return


