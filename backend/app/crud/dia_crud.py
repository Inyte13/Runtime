from datetime import date
from typing import Sequence

from backend.app.models.dia import Dia
from backend.app.schemas.dia_schema import DiaUpdate
from sqlmodel import Session, select


def create_dia(session: Session, dia: Dia) -> Dia:
  session.add(dia)
  session.commit()
  session.refresh(dia)
  return dia


def read_dia(session: Session, fecha: date) -> Dia | None:
  return session.get(Dia, fecha)


def read_dias(session: Session) -> Sequence[Dia]:
  return session.exec(select(Dia)).all()


def update_dia(session: Session, dia_bd: Dia, dia: DiaUpdate) -> Dia:
  new_dia = dia.model_dump(exclude_unset=True)
  dia_bd.sqlmodel_update(new_dia)
  session.add(dia_bd)
  session.commit()
  session.refresh(dia_bd)
  return dia_bd
