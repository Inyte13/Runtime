from pydantic import field_validator
from sqlmodel import SQLModel

from app.models.actividad import ActividadBase

# TODO: Validar el regex para mayor seguridad
class ActividadCreate(ActividadBase):
  @field_validator("nombre")
  def to_lowercase_and_not_empty(cls, v: str) -> str:
    if v.strip() == "":
      raise ValueError("El nombre no puede estar vacío")
    return v.lower()

  @field_validator("color")
  def color_not_empty(cls, v: str) -> str:
    if v.strip() == "":
      raise ValueError("El color no puede estar vacío")
    return v


class ActividadRead(ActividadBase):
  id: int


class ActividadUpdate(SQLModel):
  nombre: str | None = None
  color: str | None = None
  is_active: bool | None = None

  @field_validator("nombre")
  def to_lowercase_and_not_empty(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == "":
        raise ValueError("El nombre no puede estar vacío")
      return v.lower()
    return v

  @field_validator("color")
  def color_not_empty(cls, v: str | None) -> str | None:
    if v is not None and v.strip() == "":
      raise ValueError("El color no puede estar vacío")
    return v
