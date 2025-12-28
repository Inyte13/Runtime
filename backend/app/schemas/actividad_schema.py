from app.models.actividad import ActividadBase


class ActividadCreate(ActividadBase):
  pass


class ActividadRead(ActividadBase):
  id: int
