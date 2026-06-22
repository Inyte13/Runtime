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


class ActividadResponse(BaseModel):
  # Si no lo armo yo, va
  model_config = {'from_attributes': True}
  id: uuid.UUID
  nombre: str


# Se justifica la creación de otro schema para ahorrarnos la consulta de tiene_bloques
class ActividadResponseDetail(ActividadResponse):
  eliminable: bool = True


class ActividadResumen(BaseModel):
  id: uuid.UUID
  duracion: float
  descripciones: list[str] = []


class ActividadUpdate(BaseModel):
  nombre: str | None = Field(default=None, min_length=2, max_length=25)
  id_categoria: uuid.UUID | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('nombre')
  def validar_nombre(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('nombre no puede ser null')
    if v.strip() == '':
      raise ValueError('El nombre no puede estar vacío')
    return v.lower()

  @field_validator('id_categoria')
  def validar_id_categoria(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('id_categoria no puede ser null')
    return v
