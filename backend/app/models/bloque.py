from datetime import date, time
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.actividad import Actividad

if TYPE_CHECKING:
  from app.models.dia import Dia


class Bloque(SQLModel, table=True):
  # Tiene que ser | None, porque sqlite le asigna el id
  # No tiene el nullable=False porque sqlite lo gestiona
  id: int | None = Field(default=None, primary_key=True)
  hora: time = Field(nullable=False)
  hora_fin: time = Field(nullable=False)
  duracion: float = Field(nullable=False)

  descripcion: str | None = Field(default=None, max_length=255)

  # Tenemos id_dia (fecha) a pesar de tener dia porque es FK
  fecha: date = Field(foreign_key='dia.fecha', nullable=False)
  # Tenemos id_actividad a pesar de tener actividad porque es FK
  id_actividad: int = Field(foreign_key='actividad.id', nullable=False)
  
  # No tienen el nullable=False porque son Relationship
  
  # Bloque sabe su dia y Dia sabe sus bloques
  dia: 'Dia' = Relationship(back_populates='bloques')
  # Bloque sabe la actividad pero Actividad no sabe nada
  actividad: Actividad = Relationship()
