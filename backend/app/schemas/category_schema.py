import uuid

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types import Color

from app.domain.colors import color_normalize
from app.schemas.activity_schema import (
  ActivityCalendar,
  ActivityResponseDetail,
)


class CategoryCreate(BaseModel):
  name: str = Field(min_length=2, max_length=25)
  color: Color

  @field_validator('name')
  def validate_name(cls, v: str) -> str:
    v = v.strip()
    if v == '':
      raise ValueError('name no puede estar vacío')
    return v.lower()

  @field_validator('color')
  def validate_color(cls, v: Color) -> Color:
    return color_normalize(v)


class CategoryResponse(BaseModel):
  # Si no lo armo yo, va
  model_config = {'from_attributes': True}
  id: uuid.UUID
  name: str
  color: Color


class CategoryResponseDetail(CategoryResponse):
  activities: list[ActivityResponseDetail]
  deletable: bool = True


class CategoryCalendar(BaseModel):
  id: uuid.UUID
  duration: float
  activities: list[ActivityCalendar]


class CategoryUpdate(BaseModel):
  name: str | None = Field(default=None, min_length=2, max_length=25)
  color: Color | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('name')
  def validate_name(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('name no puede ser null')
    v = v.strip()
    if v == '':
      raise ValueError('name no puede estar vacío')
    return v.lower()

  @field_validator('color')
  def validate_color(cls, v: Color | None) -> Color:
    if v is None:
      raise ValueError('color no puede ser null')
    return color_normalize(v)
