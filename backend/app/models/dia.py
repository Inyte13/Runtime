from datetime import date
from enum import IntEnum

from backend.app.models.bloque import Bloque
from sqlmodel import Field, Relationship, SQLModel


class Estado(IntEnum):
  MAL = 1
  NORMAL = 2
  BIEN = 3


class DiaBase(SQLModel):
  titulo: str | None = Field(max_length=150, default=None)
  estado: Estado = Field(default=Estado.NORMAL)


class Dia(DiaBase, table=True):
  fecha: date = Field(primary_key=True)
  bloques: list["Bloque"] = Relationship(back_populates="dia")
