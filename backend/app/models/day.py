import uuid
from datetime import date

from app.core.database import Base
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column


class Day(Base):
  __tablename__ = 'days'
  __table_args__ = (PrimaryKeyConstraint('date', 'user_id'),)

  date: Mapped[date]
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )

  title: Mapped[str | None] = mapped_column(String(50))
