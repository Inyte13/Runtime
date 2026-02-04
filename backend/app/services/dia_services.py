from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.dia_crud import create_dia, delete_dia, read_dia, read_dias, update_dia
from app.models.dia import Dia
from app.schemas.dia_schema import DiaCreate, DiaUpdate
from app.services.configuracion_service import buscar_configuracion


def registrar_dia(session: Session, dia: DiaCreate) -> Dia:
  # No se utiliza buscar_dia, por que sale la exception
  if read_dia(session, dia.fecha):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El día ya existe")
  config = buscar_configuracion(session)
  new_dia = Dia(
    fecha=dia.fecha, titulo=config.titulo_default, estado=config.estado_default
  )
  return create_dia(session, new_dia)


def buscar_dia(session: Session, fecha: date) -> Dia:
  dia = read_dia(session, fecha)
  if not dia:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el día"
    )
  return dia


def mostrar_dias(
  session: Session, fecha_inicio: date, fecha_final: date
) -> Sequence[Dia]:
  nro_dias = (fecha_final - fecha_inicio).days
  if nro_dias > 365:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail="El rango debe ser menor a 1 año"
    )
  dias = read_dias(session, fecha_inicio, fecha_final)
  return dias


def actualizar_dia(session: Session, fecha: date, dia: DiaUpdate) -> Dia:
  dia_bd = buscar_dia(session, fecha)
  return update_dia(session, dia_bd, dia)


def eliminar_dia(session: Session, fecha: date) -> None:
  dia = buscar_dia(session, fecha)
  delete_dia(session, dia)
  return
