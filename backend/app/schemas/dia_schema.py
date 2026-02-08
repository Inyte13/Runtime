from pydantic import ConfigDict
from sqlmodel import SQLModel

from app.models.dia import DiaBase, Estado
from app.schemas.bloque_schema import BloqueRead


class DiaCreate(DiaBase):
  pass


class DiaUpdate(SQLModel):
  titulo: str | None = None
  estado: Estado | None = None


class DiaRead(DiaBase):
  model_config = ConfigDict(from_attributes=True)  # type: ignore
  # class Config:
  #   orm_mode = True


class DiaReadDetail(DiaBase):
  bloques: list[BloqueRead] = []
