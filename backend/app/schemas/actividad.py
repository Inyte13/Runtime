import uuid

from pydantic import BaseModel, Field, field_validator


class ActividadCreate(BaseModel):
  nombre: str = Field(min_length=2, max_length=25)
  id_categoria: uuid.UUID

  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('El nombre no puede estar vacío')
    return v.lower()


class ActividadRead(BaseModel):
  # Solo va en Read porque es lo que respondemos, mandamos al usuario
  model_config = {'from_attributes': True}
  id: uuid.UUID
  nombre: str = Field(min_length=2, max_length=25)
  is_active: bool


class ActividadReadDetail(ActividadRead):
  tiene_bloques: bool


class ActividadResumen(BaseModel):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  duracion: float
  descripciones: list[str] = []


class ActividadUpdate(BaseModel):
  nombre: str | None = Field(default=None, min_length=2, max_length=25)
  is_active: bool | None = None
  id_categoria: uuid.UUID | None = None

  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        raise ValueError('El nombre no puede estar vacío')
      return v.lower()
    return v
