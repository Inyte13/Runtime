from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.dia_crud import (
  create_dia,
  delete_dia,
  read_dia,
  read_dia_detail,
  read_dias,
  update_dia,
)
from app.models.dia import Dia
from app.schemas.dia_schema import DiaUpdate


def buscar_dia(session: Session, fecha: date) -> Dia:
  dia = read_dia(session, fecha)
  if not dia:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='No se encontró el día'
    )
  return dia


def buscar_dia_detail(session: Session, fecha: date) -> Dia:
  dia = read_dia_detail(session, fecha)
  if not dia:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='No se encontró el día detail',
    )
  return dia


def mostrar_dias(session: Session, inicio: date, final: date) -> Sequence[Dia]:
  nro_dias = (final - inicio).days
  # Solo se puede mostrar máximo 1 año
  if nro_dias > 365:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='El rango debe ser menor a 1 año',
    )
  return read_dias(session, inicio, final)


def actualizar_dia(session: Session, fecha: date, dia: DiaUpdate) -> Dia:
  # No se utiliza buscar_dia, por que sale la exception
  dia_bd = read_dia(session, fecha)
  # UPSERT: Si no existe lo creamos
  if not dia_bd:
    # Solo usa los campos que se declararon
    datos = dia.model_dump(exclude_unset=True)
    # KWARGS: Granularmente actualiza los campos que sobrevivieron
    new_dia = Dia(fecha=fecha, **datos)
    return create_dia(session, new_dia)
  # Si ya existe actualizamos normal
  return update_dia(session, dia_bd, dia)


def eliminar_dia(session: Session, fecha: date) -> None:
  dia = buscar_dia(session, fecha)
  delete_dia(session, dia)
  return
