import uuid
from datetime import date

from app.core.database import Base
from app.models.block import Block
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Day(Base):
  __tablename__ = 'days'
  __table_args__ = (PrimaryKeyConstraint('date', 'user_id'),)

  date: Mapped[date]
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )

  title: Mapped[str | None] = mapped_column(String(50))
  blocks: Mapped[list[Block]] = relationship(
    cascade='all, delete-orphan',  # Al delete Day, sus blocks se eliminan
    order_by=Block.hour,  # Trae los blocks ordenados
  )
