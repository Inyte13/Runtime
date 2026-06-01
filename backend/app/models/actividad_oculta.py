import uuid

from app.core.database import Base
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column


class ActividadOculta(Base):
  __tablename__ = 'actividades_ocultas'
  __table_args__ = (PrimaryKeyConstraint('id_usuario', 'id_actividad'),)
  id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey('usuarios.id'))
  id_actividad: Mapped[uuid.UUID] = mapped_column(ForeignKey('actividades.id'))
