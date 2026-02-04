from datetime import date
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from app.models.bloque import Bloque


class Estado(IntEnum):
  MAL = 1
  NORMAL = 2
  BIEN = 3


class DiaBase(SQLModel):
  titulo: str | None = Field(max_length=150, default=None)
  estado: Estado = Field(default=Estado.NORMAL)
  fecha: date = Field(primary_key=True)


class Dia(DiaBase, table=True):
  fecha: date = Field(primary_key=True)
  bloques: list["Bloque"] = Relationship(back_populates="dia")
