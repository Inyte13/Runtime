from sqlmodel import SQLModel
from app.models.dia import Dia, DiaBase, Estado


class DiaCreate(DiaBase):
  pass


class DiaRead(Dia):
  pass


class DiaUpdate(SQLModel):
  titulo: str | None = None
  estado: Estado | None = None
