import uuid

from pydantic import BaseModel, Field, field_validator


class ActivityCreate(BaseModel):
  name: str = Field(min_length=2, max_length=25)
  category_id: uuid.UUID

  @field_validator('name')
  def validate_name(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('name no puede estar vacío')
    return v.lower()


class ActivityResponse(BaseModel):
  # Si no lo armo yo, va
  model_config = {'from_attributes': True}
  id: uuid.UUID
  name: str


# Se justifica la creación de otro schema para ahorrarnos la consulta de deletable
class ActivityResponseDetail(ActivityResponse):
  deletable: bool = True


class ActivityCalendar(BaseModel):
  id: uuid.UUID
  duration: float
  descriptions: list[str] = Field(default_factory=list)  # En lugar de = []


class ActivityUpdate(BaseModel):
  name: str | None = Field(default=None, min_length=2, max_length=25)
  category_id: uuid.UUID | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('name')
  def validate_name(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('name no puede ser null')
    if v.strip() == '':
      raise ValueError('name no puede estar vacío')
    return v.lower()

  @field_validator('category_id')
  def validate_category_id(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('category_id no puede ser null')
    return v
