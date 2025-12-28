from sqlmodel import SQLModel
from app.models.actividad import ActividadBase


class ActividadCreate(ActividadBase):
  pass


class ActividadRead(ActividadBase):
  id: int


class ActividadUpdate(SQLModel):
  nombre: str | None = None
  color: str | None = None
  is_active: bool | None = None