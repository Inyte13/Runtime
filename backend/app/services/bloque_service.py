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
from app.schemas.dia_schema import DiaCreate
from app.services.dia_services import registrar_dia


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


def _calcular_hora_fin(fecha: date, hora: time, duracion: float | None) -> time | None:
  if duracion is None:
    return None
  inicio = datetime.combine(fecha, hora)
  fin = inicio + timedelta(hours=duracion)
  return fin.time()


# Horas: 3600, minutos: 60
def _calcular_duracion(session: Session, actual: Bloque, unidad_tiempo=3600) -> None:
  inicio = datetime.combine(actual.fecha, actual.hora)
  # Si ya tiene una duración, solo calculo la hora_fin
  if actual.duracion:
    actual.hora_fin = _calcular_hora_fin(actual.fecha, actual.hora, actual.duracion)
  else:
    # Si no hay duración uso al siguiente para calcularla
    siguiente = _bloque_siguiente(session, actual.fecha, actual.hora)
    if siguiente:
      fin = datetime.combine(siguiente.fecha, siguiente.hora)
      actual.duracion = (fin - inicio).total_seconds() / unidad_tiempo
      actual.hora_fin = fin.time()
    else:
      # Si no hay siguiente
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


def _validar_hora(
  session: Session, fecha: date, hora: time, duracion: float | None
) -> None:
  hora_fin = _calcular_hora_fin(fecha, hora, duracion)
  anterior = _bloque_anterior(session, fecha, hora)
  if anterior:
    if anterior.hora_fin and hora < anterior.hora_fin:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La hora debe ser posterior a {anterior.hora.strftime('%H:%M')}",
      )
    if anterior.hora_fin and hora != anterior.hora_fin:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La hora final debe ser igual a la hora inicio del anterior bloque ({anterior.hora_fin.strftime('%H:%M')})",
      )
  siguiente = _bloque_siguiente(session, fecha, hora)
  if siguiente and hora_fin and hora_fin > siguiente.hora:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"La hora_fin debe ser anterior a {siguiente.hora.strftime('%H:%M')}",
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
  fecha = bloque.fecha or date.today()
  # Primero revisaremos si existe un dia
  dia = read_dia(session, fecha)
  # Si no existe creamos uno
  if not dia:
    dia = registrar_dia(session, DiaCreate(fecha=fecha))
  
  # Segundo revisamos el último bloque del día
  statement = select(Bloque).where(Bloque.fecha == fecha).order_by(desc(Bloque.hora))
  ultimo_bloque = session.exec(statement).first()
  
  # Si el usuario manda 
  id_actividad = bloque.id_actividad
  
  # Si no hay ningún bloque
  if not ultimo_bloque:
    # Le ponemos hora 00:00
    hora = time(0, 0)
    if id_actividad is None:
      id_actividad = 1
  else:
    if ultimo_bloque.hora_fin is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No se puede crear un bloque sin antes definir la duración del anterior')
    hora = ultimo_bloque.hora_fin
    if id_actividad is None:
      id_actividad = 2

  _validar_actividad(session, id_actividad)
  _validar_hora_granulidad(hora, unidad_bloque=30)
  _validar_hora(session, fecha, hora, bloque.duracion)

  new_bloque = Bloque(
    hora=hora,
    descripcion=bloque.descripcion,
    id_actividad=id_actividad,
    fecha=fecha,
    duracion=bloque.duracion,
  )
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

    _validar_hora(session, bloque_bd.fecha, bloque.hora, bloque.duracion)
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
