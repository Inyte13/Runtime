from datetime import date
from typing import Sequence

from sqlmodel import Session, select

from app.models.bloque import Bloque
from app.schemas.bloque_schema import BloqueUpdate


def create_bloque(session: Session, bloque: Bloque) -> Bloque:
  session.add(bloque)
  session.commit()
  session.refresh(bloque)
  return bloque


def read_bloque_by_id(session: Session, id: int) -> Bloque | None:
  return session.get(Bloque, id)


def read_bloques_by_fecha(session: Session, fecha: date) -> Sequence[Bloque]:
  statement = select(Bloque).where(Bloque.fecha == fecha)
  return session.exec(statement).all()


# TODO: Agregar cuando se añada el schema para el diaCalendario
# def read_bloques_by_range(
#   session: Session, inicio: date, final: date
# ) -> Sequence[Bloque]:
#   statement = select(Bloque).where(Bloque.fecha >= inicio, Bloque.fecha <= final)
#   return session.exec(statement).all()


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
  return
