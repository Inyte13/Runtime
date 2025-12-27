from datetime import time
from sqlmodel import SQLModel, Field
from app.models.bloque import BloqueBase

# No copiamos tal cual el BloqueBase solo sin la fecha,
# sino que necesita menos indicaciones ya que no es para una bd sino para pydantic
class BloqueCreate(SQLModel):
  hora: time
  # Aquí si va porque es validación de datos, no indicaciones para la bd
  descripcion: str | None = Field(
    default=None,
    max_length=255
  )
  id_actividad: int