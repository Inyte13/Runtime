from datetime import date, time

from pydantic import field_serializer
from sqlmodel import Field, SQLModel

from app.schemas.actividad_schema import ActividadRead


# No copiamos tal cual el BloqueBase solo sin la fecha,
# sino que necesita menos indicaciones ya que no es para una bd sino para pydantic
class BloqueCreate(SQLModel):
  hora: time
  # Aquí si va porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(default=None, max_length=255)
  id_actividad: int
  fecha: date | None = None


class BloqueRead(SQLModel):
  id: int | None
  fecha: date
  hora: time | None 
  descripcion: str | None = None
  actividad: ActividadRead | None
  duracion: float | None = None
  # Se define en router
  hora_fin: time | None = None

  @field_serializer('hora', 'hora_fin')
  def formatear_hora(self, value: time | None) -> str | None:
    return value.strftime('%H:%M') if value else None
  
  class Config:
    orm_mode = True


class BloqueUpdate(SQLModel):
  hora: time | None = None
  descripcion: str | None = None
  id_actividad: int | None = None
