from sqlmodel import SQLModel

from app.models.configuracion import DiaDefaultBase
from app.models.dia import Estado


class DiaDefaultRead(DiaDefaultBase):
  pass


class DiaDefaultUpdate(SQLModel):
  # ¿Por qué no es 'Empty' y Estado.NORMAL?
  # Porque si el cliente solo modifica uno, el otro no tiene que cambiar nada
  titulo_default: str | None = None
  estado_default: Estado | None = None
