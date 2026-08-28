import uuid
from datetime import date, time

from app.core.database import Base
from app.models.activity import Activity
from sqlalchemy import ForeignKey, ForeignKeyConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Block(Base):
  __tablename__ = 'blocks'
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
      ondelete='RESTRICT',  # No puedes eliminar una activity si esta aquí
    )
  )

  activity: Mapped[Activity] = relationship()
