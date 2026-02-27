from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel

from app.models.dia import DiaBase, Estado
from app.schemas.bloque_schema import BloqueRead

# DiaCreate? NO por que ya no valido el json que recibia POST(ya no existe)


class DiaUpdate(SQLModel):
  titulo: str | None = None
  estado: Estado | None = None

  # Validator para que el '' se convierta en None
  @field_validator('titulo')
  @classmethod
  def empty_sring_to_none(cls, v):
    if v == '':
      return None
    return v


class DiaRead(DiaBase):
  model_config = ConfigDict(from_attributes=True)  # type: ignore
  # class Config:
  #   orm_mode = True


class DiaReadDetail(DiaBase):
  bloques: list[BloqueRead] = []
