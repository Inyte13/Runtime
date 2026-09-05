import uuid
from datetime import date, time
from typing import Literal

from pydantic import BaseModel, Field, field_serializer, field_validator

from app.core.constants import GRANULARITY_HOURS, GRANULARITY_MINUTES


class EdgePosition(BaseModel):
  position: Literal['end']


class RelativePosition(BaseModel):
  position: Literal['before', 'after']
  target_id: uuid.UUID


class BlockCreate(BaseModel):
  date: date
  duration: float = Field(default=GRANULARITY_HOURS, gt=0, le=24)
  description: str | None = Field(default=None, max_length=255)
  # Con discriminator compara primero con position, ya sea end, before o after
  placement: EdgePosition | RelativePosition = Field(discriminator='position')

  @field_validator('duration')
  def validate_duracion(cls, v: float) -> float:
    if (v * 60) % GRANULARITY_MINUTES != 0:
      raise ValueError(
        f'duration debe ser múltiplo de {GRANULARITY_MINUTES} minutos'
      )
    return v

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      v = v.strip()
      if v == '':
        return None
    return v


class BlockResponse(BaseModel):
  model_config = {'from_attributes': True}

  id: uuid.UUID
  hour: time
  hour_end: time
  duration: float
  description: str | None = None
  activity_id: uuid.UUID

  # Transforma el time(8,30) en '08:30' para el frontend
  @field_serializer('hour', 'hour_end')
  def validate_hour(self, value: time | None) -> str | None:
    return value.strftime('%H:%M') if value else None


class BlockUpdate(BaseModel):
  duration: float | None = Field(default=None, ge=GRANULARITY_HOURS, le=24)
  description: str | None = None
  activity_id: uuid.UUID | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('duration')
  def validate_duration(cls, v: float | None) -> float | None:
    if v is None:
      raise ValueError('duration no puede ser null')
    if (v * 60) % GRANULARITY_MINUTES != 0:
      raise ValueError(
        f'duration debe ser múltiplo de {GRANULARITY_MINUTES} minutos'
      )
    return v

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      v = v.strip()
      if v == '':
        return None
    return v

  @field_validator('activity_id')
  def validate_activity_id(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('activity_id no puede ser null')
    return v
