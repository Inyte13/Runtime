from datetime import date, time

from fastapi import HTTPException, status
from sqlmodel import Session, desc, select

from app.crud.bloque_crud import read_bloque_by_id
from app.models.actividad import Actividad
from app.models.bloque import Bloque


def buscar_bloque(session: Session, id: int) -> Bloque:
  bloque = read_bloque_by_id(session, id)
  if not bloque:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Bloque no encontrado"
    )
  return bloque


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
