from datetime import date, time

from pydantic import ConfigDict, field_serializer, field_validator
from sqlmodel import Field, SQLModel

from app.schemas.actividad_schema import ActividadRead


# Necesita menos indicaciones ya que no es para una bd sino para pydantic
class BloqueCreate(SQLModel):
  hora: time | None = None
  # Aquí si va porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(default=None, max_length=255)
  id_actividad: int | None = None
  fecha: date | None = None
  duracion: float | None = None
  # Validator para que el '' se convierta en None
  @field_validator('descripcion')
  @classmethod
  def empty_sring_to_none(cls, v):
    if v == '':
      return None
    return v


class BloqueRead(SQLModel):
  id: int | None
  hora: time | None 
  descripcion: str | None = None
  actividad: ActividadRead | None
  duracion: float | None = None
  hora_fin: time | None = None

  @field_serializer('hora', 'hora_fin')
  def formatear_hora(self, value: time | None) -> str | None:
    return value.strftime('%H:%M') if value else None
  
  model_config = ConfigDict(from_attributes=True) # type: ignore
  # class Config:
  #   orm_mode = True


class BloqueUpdate(SQLModel):
  hora: time | None = None
  descripcion: str | None = None
  id_actividad: int | None = None
  duracion: float | None = None
