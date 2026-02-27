from datetime import date
from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, select

from app.models.dia import Dia
from app.schemas.dia_schema import DiaUpdate


def read_dia(session: Session, fecha: date) -> Dia | None:
  # Lazy loading
  return session.get(Dia, fecha)


def read_dia_detail(session: Session, fecha: date) -> Dia | None:
  # Eager loading
  statement = (
    select(Dia).where(Dia.fecha == fecha).options(selectinload(Dia.bloques))  # type: ignore
  )
  return session.exec(statement).first()
  statement = (
    select(Dia)
    .where(fecha_inicio <= Dia.fecha)
    .where(Dia.fecha <= fecha_fin)
    .order_by(col(Dia.fecha))
  )
  return session.exec(statement).all()


def update_dia(session: Session, dia_bd: Dia, dia: DiaUpdate) -> Dia:
  new_dia = dia.model_dump(exclude_unset=True)
  dia_bd.sqlmodel_update(new_dia)
  session.add(dia_bd)
  session.commit()
  session.refresh(dia_bd)
  return dia_bd


def delete_dia(session: Session, dia: Dia) -> None:
  session.delete(dia)
  session.commit()
  return