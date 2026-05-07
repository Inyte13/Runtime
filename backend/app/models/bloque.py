import uuid
from datetime import date, time

from app.core.database import Base
from app.models.actividad import Actividad
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Bloque(Base):
  __tablename__ = 'bloques'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,  # cross-database
    primary_key=True,
    default=uuid.uuid4,
  )
  hora: Mapped[time]
  hora_fin: Mapped[time]
  duracion: Mapped[float]
  descripcion: Mapped[str | None] = mapped_column(String(255))
  fecha: Mapped[date] = mapped_column(ForeignKey('dias.fecha'))
  id_actividad: Mapped[uuid.UUID] = mapped_column(ForeignKey('actividades.id'))

  actividad: Mapped[Actividad] = relationship()
