from datetime import date, time

from backend.app.models.actividad import Actividad
from sqlmodel import Field, Relationship, SQLModel


class BloqueBase(SQLModel):
  fecha: date = Field(default_factory=date.today, index=True)
  hora: time = Field(index=True)
  descripcion: str | None = Field(default=None, max_length=255)
  # Foreign key
  id_actividad: int = Field(foreign_key="actividad.id", nullable=False)
  actividad: Actividad | None = Relationship()


class Bloque(BloqueBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
