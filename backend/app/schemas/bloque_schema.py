from datetime import date, time

from pydantic import field_serializer, field_validator
from sqlmodel import Field, SQLModel

from app.schemas.actividad_schema import ActividadRead


# Necesita menos indicaciones porque no tiene tabla
class BloqueCreate(SQLModel):
  duracion: float = 0.5
  # TODO: Validator para que envie mas del multiplo de 0.5 o lo que escoja

  # Aquí si va porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(default=None, max_length=255)
  # Si no viene usa el la fecha actual
  fecha: date = Field(default_factory=date.today)
  # Podemos recibir None pero lo controlaremos en el backend
  id_actividad: int | None = None
  id_ref: int | None = None

  # Validator para que el '' se convierta en None
  @field_validator('descripcion')
  @classmethod
  def formatear_str_vacio(cls, v):
    if v == '':
      return None
    return v

  @field_validator('duracion')
  @classmethod
  def duracion_valida(cls, v: float) -> float:
    if v <= 0:
      raise ValueError('La duración debe ser mayor que 0')
    if (v * 60) % 30 != 0:
      raise ValueError('La duración debe ser múltiplo de 30 minutos')
    return v


class BloqueRead(SQLModel):
  id: int
  hora: time
  descripcion: str | None = None
  duracion: float
  hora_fin: time
  id_actividad: int

  # Transforma el time(8,30) en '08:30'
  @field_serializer('hora', 'hora_fin')
  def formatear_hora(self, value: time | None) -> str | None:
    return value.strftime('%H:%M') if value else None


class BloqueUpdate(SQLModel):
  descripcion: str | None = None
  id_actividad: int | None = None
  duracion: float | None = None

  # Validator para que el '' se convierta en None
  @field_validator('descripcion')
  @classmethod
  def formatear_str_vacio(cls, v):
    if v == '':
      return None
    return v

  @field_validator('duracion')
  @classmethod
  def duracion_valida(cls, v: float) -> float:
    if v <= 0:
      raise ValueError('La duración debe ser mayor que 0')
    if (v * 60) % 30 != 0:
      raise ValueError('La duración debe ser múltiplo de 30 minutos')
    return v
