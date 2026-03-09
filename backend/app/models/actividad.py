from sqlmodel import Field, SQLModel


class Actividad(SQLModel, table=True):
  # Tiene que ser | None, porque sqlite le asigna el id
  # No tiene el nullable=False porque sqlite lo gestiona
  id: int | None = Field(default=None, primary_key=True)
  nombre: str = Field(index=True, unique=True, max_length=50, nullable=False)
  color: str = Field(max_length=7, default='#0191f1', nullable=False)
  is_active: bool = Field(default=True, nullable=False)
