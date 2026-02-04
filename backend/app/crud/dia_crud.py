from datetime import date
from typing import Sequence

from sqlmodel import Session, select

from app.models.dia import Dia
from app.schemas.dia_schema import DiaUpdate


def create_dia(session: Session, dia: Dia) -> Dia:
  session.add(dia)
  session.commit()
  session.refresh(dia)
  return dia


def read_dia(session: Session, fecha: date) -> Dia | None:
  return session.get(Dia, fecha)


def read_dias(session: Session, fecha_inicio: date, fecha_fin: date) -> Sequence[Dia]:
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