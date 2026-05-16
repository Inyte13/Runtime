from pydantic import field_validator
from sqlmodel import SQLModel


class ActividadCreate(SQLModel):
  nombre: str
  id_categoria: int

  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('El nombre no puede estar vacío')
    return v.lower()


class ActividadRead(SQLModel):
  id: int
  nombre: str
  is_archived: bool


class ActividadReadDetail(ActividadRead):
  tiene_bloques: bool


class ActividadResumen(SQLModel):
  id: int
  duracion: float
  descripciones: list[str] = []


class ActividadUpdate(SQLModel):
  nombre: str | None = None
  is_archived: bool | None = None
  id_categoria: int | None = None

  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        raise ValueError('El nombre no puede estar vacío')
      return v.lower()
    return v
