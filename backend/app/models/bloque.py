import uuid
from datetime import date, time

from app.core.database import Base
from app.models.actividad import Actividad
from sqlalchemy import ForeignKey, ForeignKeyConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Bloque(Base):
  __tablename__ = 'bloques'
  __table_args__ = (
    ForeignKeyConstraint(
      ['fecha', 'id_usuario'],
      ['dias.fecha', 'dias.id_usuario'],
      ondelete='CASCADE',
    ),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  id_usuario: Mapped[uuid.UUID]
  fecha: Mapped[date]
  hora: Mapped[time]
  hora_fin: Mapped[time]
  duracion: Mapped[float]
  descripcion: Mapped[str | None] = mapped_column(String(255))
  id_actividad: Mapped[uuid.UUID] = mapped_column(
    ForeignKey(
      'actividades.id',
      ondelete='RESTRICT',  # No puedes eliminar una actividad si esta aquí
    )
  )

  actividad: Mapped[Actividad] = relationship()
