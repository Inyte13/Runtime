from sqlmodel import Field, SQLModel

from app.models.dia import Estado


class DiaDefaultBase(SQLModel):
  titulo_default: str | None = Field(default="Empty", max_length=150)
  estado_default: Estado = Field(default=Estado.NORMAL)


class DiaDefault(DiaDefaultBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
