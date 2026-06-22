import uuid

from app.core.database import Base
from app.models.actividad import Actividad
from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categoria(Base):
  __tablename__ = 'categorias'
  # Pares únicos
  __table_args__ = (
    UniqueConstraint(
      'nombre', 'id_usuario', name='uq_categoria_nombre_usuario'
    ),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  id_usuario: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('usuarios.id', ondelete='CASCADE')
  )

  nombre: Mapped[str] = mapped_column(String(25))
  color: Mapped[str] = mapped_column(String(7))

  actividades: Mapped[list[Actividad]] = relationship(
    cascade='all, delete-orphan',  # Al eliminar Categoria, sus actividades se eliminan
  )
