from datetime import date, datetime, time, timedelta
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud.bloque_crud import read_bloques_by_fecha
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


def recalcular_hora_final(
  session: Session, fecha: date, ids: list[int]
) -> None:
  bloques = read_bloques_by_fecha(session, fecha)

  if not bloques:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail='No hay bloques que ordenar'
    )

  # Sacamos los id y lo convertimos a set para comparar con los que nos viene
  if {bloque.id for bloque in bloques} != set(ids):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='Los bloques no coinciden'
    )

  # Dict para búsqueda rapida
  bloques_dict = {bloque.id: bloque for bloque in bloques}

  hora_temp = datetime.combine(fecha, time(0, 0))

  for i, id in enumerate(ids):
    bloque = bloques_dict[id]
    bloque.hora = hora_temp.time()

    if bloque.duracion is not None:
      hora_temp += timedelta(hours=bloque.duracion)
      bloque.hora_fin = hora_temp.time()

    else:
      bloque.hora_fin = None
      if i != len(ids) - 1:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail='El bloque sin duración solo puede ir al final del día',
        )
    session.add(bloque)
  session.commit()
  return


def eliminar_dia(session: Session, fecha: date) -> None:
  dia = buscar_dia(session, fecha)
  delete_dia(session, dia)
  return
