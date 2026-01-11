from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlmodel import Session, desc, select

from app.crud.bloque_crud import (
  create_bloque,
  delete_bloque,
  read_bloque_by_id,
  update_bloque,
)
from app.crud.dia_crud import read_dia
from app.models.actividad import Actividad
from app.models.bloque import Bloque
from app.schemas.actividad_schema import ActividadRead
from app.schemas.bloque_schema import BloqueCreate, BloqueRead, BloqueUpdate
from app.services.dia_services import generar_dia


# Horas: 3600, minutos: 60
def _calcular_duracion(session: Session, bloque: Bloque, unidad_tiempo=3600) -> None:
  statement = (
    select(Bloque)
    .where(Bloque.fecha == bloque.fecha, Bloque.hora > bloque.hora)
    .order_by(Bloque.hora)  # type: ignore
  )
  siguiente = session.exec(statement).first()

  if siguiente:
    inicio = datetime.combine(bloque.fecha, bloque.hora)
    fin = datetime.combine(siguiente.fecha, siguiente.hora)
    bloque.duracion = (fin - inicio).total_seconds() / unidad_tiempo
  else:
    bloque.duracion = None
  session.add(bloque)

  statement = (
    select(Bloque)
    .where(Bloque.fecha == bloque.fecha, Bloque.hora < bloque.hora)
    .order_by(Bloque.hora.desc())  # type: ignore
  )
  anterior = session.exec(statement).first()

  if anterior:
    inicio = datetime.combine(anterior.fecha, anterior.hora)
    fin = datetime.combine(bloque.fecha, bloque.hora)
    anterior.duracion = (fin - inicio).total_seconds() / unidad_tiempo
    session.add(anterior)
  session.commit()


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


def _validar_hora_superior(session: Session, fecha: date, hora: time) -> None:
  # Buscamos el último bloque registrado del dia
  statement = select(Bloque).where(Bloque.fecha == fecha).order_by(desc(Bloque.hora))
  last_bloque = session.exec(statement).first()

  if last_bloque and hora <= last_bloque.hora:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"La hora debe ser posterior a {last_bloque.hora.strftime('%H:%M')}",
    )
  return


def calcular_hora_fin(bloque: Bloque) -> BloqueRead:
  hora_fin = None
  if bloque.duracion:
    inicio = datetime.combine(bloque.fecha, bloque.hora)
    fin = inicio + timedelta(hours=bloque.duracion)
    hora_fin = fin.time()
  return BloqueRead(
    id=bloque.id,
    fecha=bloque.fecha,
    hora=bloque.hora,
    descripcion=bloque.descripcion,
    duracion=bloque.duracion,
    hora_fin=hora_fin,
    actividad=ActividadRead.model_validate(bloque.actividad),
  )


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
  _validar_hora_superior(session, fecha, bloque.hora)
  dia = read_dia(session, fecha)
  if not dia:
    dia = generar_dia(session, fecha)
  new_bloque = Bloque.model_validate({**bloque.model_dump(), "fecha": dia.fecha})
  bloque_bd = create_bloque(session, new_bloque)
  _calcular_duracion(session, bloque_bd)
  return create_bloque(session, bloque_bd)


def actualizar_bloque(session: Session, id: int, bloque: BloqueUpdate) -> Bloque:
  bloque_bd = buscar_bloque(session, id)
  # Si la actividad se ingresó y es diferente a la actual
  if bloque.id_actividad and bloque.id_actividad != bloque_bd.id_actividad:
    # Validamos la actividad ingresada
    _validar_actividad(session, bloque.id_actividad)
  # Si la hora se ingresó
  if bloque.hora:
    _validar_hora_granulidad(bloque.hora, unidad_bloque=30)

  if bloque.descripcion == '':
    bloque.descripcion = None

  bloque_bd = update_bloque(session, bloque_bd, bloque)
  _calcular_duracion(session, bloque_bd)
  return bloque_bd


def eliminar_bloque(session: Session, id: int) -> None:
  bloque = buscar_bloque(session, id)
  delete_bloque(session, bloque)
  return
