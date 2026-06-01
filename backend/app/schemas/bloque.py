import uuid
from datetime import date, time

from pydantic import BaseModel, Field, field_serializer, field_validator


class BloqueCreate(BaseModel):
  duracion: float = 0.5
  # Aqui si va el Field porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(default=None, max_length=255)
  fecha: date
  id_actividad: uuid.UUID

  # Usamos la Alternativa A: Nil UUID para representar el inicio del día
  id_ref: uuid.UUID | None = None

  @field_validator('duracion')
  def duracion_valida(cls, v: float) -> float:
    if v <= 0:
      raise ValueError('La duración debe ser mayor que 0')
    if (v * 60) % 30 != 0:
      raise ValueError('La duración debe ser múltiplo de 30 minutos')
    return v

  # Validator para que el '' se convierta en None
  @field_validator('descripcion')
  def formatear_str_vacio(cls, v: str | None) -> str | None:
    if v == '' or v is None:
      return None
    return v


class BloqueResponse(BaseModel):
  model_config = {'from_attributes': True}

  id: uuid.UUID
  hora: time
  hora_fin: time
  duracion: float
  descripcion: str | None = None
  id_actividad: uuid.UUID

  # Transforma el time(8,30) en '08:30' para el frontend
  @field_serializer('hora', 'hora_fin')
  def formatear_hora(self, value: time | None) -> str | None:
    return value.strftime('%H:%M') if value else None


class BloqueUpdate(BaseModel):
  duracion: float | None = None
  descripcion: str | None = None
  id_actividad: uuid.UUID | None = None

  @field_validator('duracion')
  def duracion_valida(cls, v: float | None) -> float | None:
    if v is None:
      raise ValueError('duracion no puede ser null')
    if v <= 0:
      raise ValueError('La duración debe ser mayor que 0')
    if (v * 60) % 30 != 0:
      raise ValueError('La duración debe ser múltiplo de 30 minutos')
    return v

  @field_validator('descripcion')
  def formatear_str_vacio(cls, v: str | None) -> str | None:
    if v == '' or v is None:
      return None
    return v

  @field_validator('id_actividad')
  def validate_id_actividad(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('id_actividad no puede ser null')
    return v
