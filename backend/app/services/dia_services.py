from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.dia_crud import create_dia, read_dia, read_dias, update_dia
from app.models.dia import Dia
from app.schemas.dia_schema import DiaUpdate
from app.services.configuracion_service import buscar_configuracion


def generar_dia(session: Session, fecha: date) -> Dia:
  if buscar_dia(session, fecha):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail="El día ya existe"
    )
  config = buscar_configuracion(session)
  new_dia = Dia(fecha=fecha, titulo=config.titulo_default, estado=config.estado_default)
  return create_dia(session, new_dia)


def buscar_dia(session: Session, fecha: date) -> Dia:
  dia = read_dia(session, fecha)
  if not dia:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el día"
    )
  return dia


def mostrar_dias(session: Session) -> Sequence[Dia]:
  dias = read_dias(session)
  if not dias:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="No se registro ningún día"
    )
  return dias


def actualizar_dia(session: Session, fecha: date, dia: DiaUpdate) -> Dia:
  dia_bd = buscar_dia(session, fecha)
  return update_dia(session, dia_bd, dia)
