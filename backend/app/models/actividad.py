import uuid

from app.core.database import Base
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class Actividad(Base):
  __tablename__ = 'actividades'
  # Pares únicos
  __table_args__ = (
    UniqueConstraint(
      'nombre', 'id_usuario', name='uq_actividad_nombre_usuario'
    ),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,  # cross-database
    primary_key=True,
    default=uuid.uuid4,
  )
  id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey('usuarios.id'))
  
  nombre: Mapped[str] = mapped_column(String(25))
  is_active: Mapped[bool] = mapped_column(Boolean, default=True)
  id_categoria: Mapped[uuid.UUID] = mapped_column(ForeignKey('categorias.id'))
