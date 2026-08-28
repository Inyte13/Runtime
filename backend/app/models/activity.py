import uuid

from app.core.database import Base
from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class Activity(Base):
  __tablename__ = 'activities'
  # Pares únicos
  __table_args__ = (
    UniqueConstraint('name', 'user_id', name='uq_activity_name_user'),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )
  category_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('categories.id', ondelete='CASCADE')
  )

  name: Mapped[str] = mapped_column(String(25))
