from datetime import date, time
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.actividad import Actividad

if TYPE_CHECKING:
  from app.models.dia import Dia


class BloqueBase(SQLModel):
  hora: time = Field(index=True)
  descripcion: str | None = Field(default=None, max_length=255)
  # Foreign key, relación 1-1
  id_actividad: int = Field(foreign_key="actividad.id", nullable=False)
  duracion: float | None = Field(default=None)
  hora_fin: time | None = Field(default=None)


class Bloque(BloqueBase, table=True):
  # Puede estar vacío en memoria antes de persistir
  id: int | None = Field(default=None, primary_key=True)
  # Foreign key, heredamos la fecha de día
  fecha: date = Field(foreign_key="dia.fecha", nullable=False)
  dia: "Dia" = Relationship(back_populates="bloques")
  actividad: Actividad | None = Relationship()
