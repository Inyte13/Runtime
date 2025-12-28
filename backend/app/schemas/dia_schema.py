from datetime import date

from app.models.dia import DiaBase


class DiaCreate(DiaBase):
  pass


class DiaRead(DiaBase):
  fecha: date
