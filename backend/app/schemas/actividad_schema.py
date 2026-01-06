from pydantic import field_validator
from sqlmodel import SQLModel

from app.models.actividad import ActividadBase


class ActividadCreate(ActividadBase):
  # Validador en Pydantic/SQLModel
  # cls = la clase
  # v = value
  @field_validator("nombre")
  def to_lowercase(cls, v: str) -> str:
    return v.lower()


class ActividadRead(ActividadBase):
  id: int


class ActividadUpdate(SQLModel):
  nombre: str | None = None
  color: str | None = None
  is_active: bool | None = None

  @field_validator("nombre")
  def to_lowercase(cls, v: str | None) -> str | None:
    return v.lower() if v else v
