from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlmodel import Session, asc, desc, select

from app.crud.bloque_crud import (
  create_bloque,
  delete_bloque,
  read_bloque_by_id,
  update_bloque,
)
from app.crud.dia_crud import read_dia
from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.schemas.bloque_schema import BloqueCreate, BloqueUpdate
from app.services.dia_services import generar_dia


def _bloque_anterior(session: Session, fecha: date, hora: time) -> Bloque | None:
  anterior = session.exec(
    select(Bloque)
    .where(
      Bloque.fecha == fecha,
      Bloque.hora < hora,
    )
    .order_by(desc(Bloque.hora))
  ).first()
  return anterior


def _bloque_siguiente(session: Session, fecha: date, hora: time) -> Bloque | None:
  siguiente = session.exec(
    select(Bloque)
    .where(
      Bloque.fecha == fecha,
      Bloque.hora > hora,
    )
    .order_by(asc(Bloque.hora))
  ).first()
  return siguiente


# Horas: 3600, minutos: 60
def _calcular_duracion(session: Session, actual: Bloque, unidad_tiempo=3600) -> None:
  """Calcula la duración y hora_fin de un bloque y ajusta la del bloque anterior"""
  inicio = datetime.combine(actual.fecha, actual.hora)

  if actual.duracion:
    fin = inicio + timedelta(hours=actual.duracion)
    actual.hora_fin = fin.time()
  else:
    siguiente = _bloque_siguiente(session, actual.fecha, actual.hora)
    if siguiente:
      fin = datetime.combine(siguiente.fecha, siguiente.hora)
      actual.duracion = (fin - inicio).total_seconds() / unidad_tiempo
      actual.hora_fin = fin.time()
    else:
      actual.duracion = None
      actual.hora_fin = None

  session.add(actual)

  anterior = _bloque_anterior(session, actual.fecha, actual.hora)
  if anterior:
    inicio_ant = datetime.combine(anterior.fecha, anterior.hora)
    fin_ant = datetime.combine(actual.fecha, actual.hora)
    anterior.duracion = (fin_ant - inicio_ant).total_seconds() / unidad_tiempo
    anterior.hora_fin = actual.hora
    session.add(anterior)

  session.commit()
  return


def _validar_hora(session: Session, fecha: date, hora: time) -> None:
  anterior = _bloque_anterior(session, fecha, hora)
  if anterior and hora <= anterior.hora:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"La hora debe ser posterior a {anterior.hora.strftime('%H:%M')}",
    )

  siguiente = _bloque_siguiente(session, fecha, hora)
  if siguiente and hora >= siguiente.hora:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"La hora debe ser anterior a {siguiente.hora.strftime('%H:%M')}",
    )
  return


def _validar_actividad(session: Session, id: int) -> None:
  actividad = session.get(Actividad, id)
  if not actividad:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada"
    )
  if not actividad.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail="La actividad está en la papelera"
    )
  return


def _validar_hora_granulidad(hora: time, unidad_bloque: int = 30) -> None:
  if hora.minute % unidad_bloque != 0 or hora.second != 0 or hora.microsecond != 0:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"La hora debe estar en múltiplos de {unidad_bloque} minutos",
    )
  return


def buscar_bloque(session: Session, id: int) -> Bloque:
  bloque = read_bloque_by_id(session, id)
  if not bloque:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Bloque no encontrado"
    )
  return bloque


def registrar_bloque(session: Session, bloque: BloqueCreate) -> Bloque:
  _validar_actividad(session, bloque.id_actividad)
  _validar_hora_granulidad(bloque.hora, unidad_bloque=30)
  fecha = bloque.fecha or date.today()
  _validar_hora(session, fecha, bloque.hora)

  dia = read_dia(session, fecha)
  if not dia:
    dia = generar_dia(session, fecha)
    
  if bloque.descripcion == "":
    bloque.descripcion = None

  new_bloque = Bloque.model_validate({**bloque.model_dump(), "fecha": dia.fecha})
  bloque_bd = create_bloque(session, new_bloque)

  _calcular_duracion(session, bloque_bd)
  return bloque_bd


def actualizar_bloque(session: Session, id: int, bloque: BloqueUpdate) -> Bloque:
  bloque_bd = buscar_bloque(session, id)
  if bloque.id_actividad:
    # Validamos la actividad ingresada
    _validar_actividad(session, bloque.id_actividad)
  # Si la hora se ingresó
  if bloque.hora:
    _validar_hora_granulidad(bloque.hora, unidad_bloque=30)
    _validar_hora(session, bloque_bd.fecha, bloque.hora)
  # Si la descripción es '' como lo manda el frontend para la bd será None
  if bloque.descripcion == "":
    bloque.descripcion = None

  bloque_bd = update_bloque(session, bloque_bd, bloque)
  _calcular_duracion(session, bloque_bd)
  return bloque_bd


def eliminar_bloque(session: Session, id: int) -> None:
  bloque = buscar_bloque(session, id)
  delete_bloque(session, bloque)
  return
