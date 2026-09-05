import uuid
from datetime import date, time

from app.core.database import Base
from sqlalchemy import ForeignKey, ForeignKeyConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column


# TODO: Índice de user_id -> date -> hour
# TODO: Índice en activity_id para búsqueda más rápida
class Block(Base):
  __tablename__ = 'blocks'
  # fk de la pk compuesta
  __table_args__ = (
    ForeignKeyConstraint(
      ['date', 'user_id'],
      ['days.date', 'days.user_id'],
      ondelete='CASCADE',
    ),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  user_id: Mapped[uuid.UUID]
  date: Mapped[date]
  hour: Mapped[time]
  hour_end: Mapped[time]
  duration: Mapped[float]
  description: Mapped[str | None] = mapped_column(String(255))
  activity_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey(
      'activities.id',
      ondelete='RESTRICT',  # No puedes eliminar una activity si lo usa un block
    )
  )
