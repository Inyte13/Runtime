from datetime import date
from enum import IntEnum
from fastapi import FastAPI
from sqlmodel import SQLModel, Field

class Estado(IntEnum):
  MAL = 1
  NORMAL = 2
  BIEN = 3

class DiaBase(SQLModel):
  titulo: str | None = Field(
    max_length=150,
    default=None
  )
  estado: Estado = Field(
    default=Estado.NORMAL
  )

class Dia(DiaBase, table=True):
  fecha: date = Field(
    primary_key=True
  )

