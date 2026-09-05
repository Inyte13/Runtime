from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.schemas.block_schema import BlockResponse
from app.schemas.category_schema import CategoryCalendar


# Para el patch
class DayResponse(BaseModel):
  model_config = {'from_attributes': True}

  date: date
  title: str | None = Field(default=None, max_length=50)

  @field_validator('title')
  def validate_title(cls, v: str | None) -> str | None:
    if v is not None:
      v = v.strip()
      if v == '':
        return None
    return v


class DayResponseDetail(DayResponse):
  blocks: list[BlockResponse]


class DayCalendar(DayResponse):
  duration: float
  categories: list[CategoryCalendar]


class DayUpdate(BaseModel):
  title: str | None = Field(default=None, max_length=50)

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente
  @field_validator('title')
  def validate_title(cls, v: str | None) -> str | None:
    if v is not None:
      v = v.strip()
      if v == '':
        return None
    return v
