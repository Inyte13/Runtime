import uuid

from app.core.database import Base
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column


class HiddenActivity(Base):
  __tablename__ = 'hidden_activities'
  __table_args__ = (PrimaryKeyConstraint('activity_id', 'user_id'),)
  activity_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('activities.id', ondelete='CASCADE')
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )
