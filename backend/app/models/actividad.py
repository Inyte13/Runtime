from sqlmodel import Field, SQLModel


# La clase base para no reescribir
class ActividadBase(SQLModel):
  nombre: str = Field(
    index=True,  # Hace que las búsquedas por nombre sean más rápidas
    unique=True,
    max_length=50,
  )
  color: str = Field(max_length=7, default="#0191f1")
  is_active: bool = Field(default=True)


class Actividad(ActividadBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
