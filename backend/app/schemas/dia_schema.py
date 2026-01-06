from datetime import date

from app.schemas.bloque_schema import BloqueRead
from sqlmodel import SQLModel

from app.models.dia import DiaBase, Estado


class DiaCreate(DiaBase):
  pass


class DiaRead(DiaBase):
  fecha: date
  bloques: list[BloqueRead] = []

  class Config:
    orm_mode = True


class DiaUpdate(SQLModel):
  titulo: str | None = None
  estado: Estado | None = None
