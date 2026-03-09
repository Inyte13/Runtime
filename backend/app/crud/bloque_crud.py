from datetime import date, time
from typing import Sequence

from sqlmodel import Session, col, select

from app.models.bloque import Bloque
from app.schemas.bloque_schema import BloqueUpdate


def create_bloque(session: Session, bloque: Bloque) -> Bloque:
  session.add(bloque)
  session.commit()
  session.refresh(bloque)
  return bloque


def read_bloque(session: Session, id: int) -> Bloque | None:
  return session.get(Bloque, id)


def read_bloques_by_range(
  session: Session,
  fecha: date,
  hora_desde: time | None = None,
  hora_hasta: time | None = None,
  # Para la cascada
  incluir_desde: bool = True,
) -> Sequence[Bloque]:
  statement = (
    select(Bloque).where(Bloque.fecha == fecha).order_by(col(Bloque.hora))
  )
  if hora_desde is not None:
    if incluir_desde:
      statement = statement.where(Bloque.hora >= hora_desde)
    else:
      # Para la cascada
      statement = statement.where(Bloque.hora > hora_desde)

  if hora_hasta is not None:
    statement = statement.where(Bloque.hora <= hora_hasta)
  return session.exec(statement).all()


def update_bloque(
  session: Session, bloque_bd: Bloque, bloque: BloqueUpdate
) -> Bloque:
  new_bloque = bloque.model_dump(exclude_unset=True)
  bloque_bd.sqlmodel_update(new_bloque)
  session.add(bloque_bd)
  session.commit()
  session.refresh(bloque_bd)
  return bloque_bd


def delete_bloque(session: Session, bloque: Bloque) -> None:
  session.delete(bloque)
  session.commit()
