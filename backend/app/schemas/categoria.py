import re
import uuid

from app.schemas.actividad import ActividadResponseDetail, ActividadResumen
from pydantic import BaseModel, field_validator


class CategoriaCreate(BaseModel):
  nombre: str
  color: str

  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('El nombre no puede estar vacío')
    return v.lower()

  @field_validator('color')
  def color_not_empty(cls, v: str) -> str:
    if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
      raise ValueError('El color debe ser un hexadecimal válido (#RRGGBB)')
    return v


class CategoriaResponse(BaseModel):
  # Si no lo armo yo, va
  model_config = {'from_attributes': True}
  id: uuid.UUID
  nombre: str
  color: str


class CategoriaResponseDetail(CategoriaResponse):
  actividades: list[ActividadResponseDetail]


class CategoriaResumen(BaseModel):
  id: uuid.UUID
  actividades: list[ActividadResumen]


class CategoriaUpdate(BaseModel):
  nombre: str | None = None
  color: str | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('nombre')
  def to_lowercase_and_not_empty(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('nombre no puede ser null')
    if v.strip() == '':
      raise ValueError('El nombre no puede estar vacío')
    return v.lower()

  @field_validator('color')
  def color_not_empty(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('color no puede ser null')
    if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
      raise ValueError('El color debe ser un hexadecimal válido (#RRGGBB)')
    return v
