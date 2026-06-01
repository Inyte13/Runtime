import uuid
from datetime import date

from app.core.database import Base
from app.models.bloque import Bloque
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Dia(Base):
  __tablename__ = 'dias'
  __table_args__ = (PrimaryKeyConstraint('fecha', 'id_usuario'),)

  fecha: Mapped[date]
  id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey('usuarios.id'))

  titulo: Mapped[str | None] = mapped_column(String(50))
  bloques: Mapped[list[Bloque]] = relationship(
    cascade='all, delete-orphan',  # Al eliminar Dia, sus bloques se eliminan
    order_by=Bloque.hora,  # Trae los bloques ordenados
  )
