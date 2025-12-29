from datetime import date, time

from sqlmodel import Field, SQLModel

from app.schemas.actividad_schema import ActividadRead


# No copiamos tal cual el BloqueBase solo sin la fecha,
# sino que necesita menos indicaciones ya que no es para una bd sino para pydantic
class BloqueCreate(SQLModel):
  hora: time
  # Aquí si va porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(default=None, max_length=255)
  id_actividad: int


class BloqueRead(SQLModel):
  id: int
  fecha: date
  hora: time
  descripcion: str | None = None
  id_actividad: int
  actividad: ActividadRead | None = None


class BloqueUpdate(SQLModel):
  hora: time | None = None
  descripcion: str | None = None
  id_actividad: int | None = None
  
