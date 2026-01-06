from datetime import date, time

from backend.app.models.dia import Dia
from sqlmodel import Field, Relationship, SQLModel

from app.models.actividad import Actividad


class BloqueBase(SQLModel):
  hora: time = Field(index=True)
  descripcion: str | None = Field(default=None, max_length=255)
  # Foreign key, relación 1-1
  id_actividad: int = Field(foreign_key="actividad.id", nullable=False)
  actividad: Actividad | None = Relationship()


class Bloque(BloqueBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  # Foreign key, heredamos la fecha de día
  fecha: date = Field(foreign_key="dia.fecha")
  dia: Dia = Relationship(back_populates="bloques")
