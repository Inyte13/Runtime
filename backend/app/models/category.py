import uuid

from app.core.database import Base
from app.models.types import ColorType
from pydantic_extra_types import Color
from sqlalchemy import ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class Category(Base):
  __tablename__ = 'categories'
  __table_args__ = (
    UniqueConstraint('name', 'user_id', name='uq_category_name_user'),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )

  name: Mapped[str] = mapped_column(String(25))
  color: Mapped[Color] = mapped_column(ColorType())
