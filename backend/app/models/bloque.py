from datetime import date, time

from sqlmodel import Field, SQLModel


class BloqueBase(SQLModel):
  fecha: date = Field(index=True)
  hora: time = Field(index=True)
  descripcion: str | None = Field(default=None, max_length=255)
  # Foreign key
  id_actividad: int = Field(foreign_key="actividad.id")


class Bloque(BloqueBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
