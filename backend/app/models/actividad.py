from sqlmodel import Field, SQLModel


class ActividadBase(SQLModel):
  nombre: str = Field(
    index=True,
    unique=True,
    max_length=50,
  )
  color: str = Field(max_length=7, default='#0191f1')
  is_active: bool = Field(default=True)


class Actividad(ActividadBase, table=True):
  # Puede estar vacío en memoria antes de persistir
  id: int = Field(default=None, primary_key=True)
