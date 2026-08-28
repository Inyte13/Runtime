import uuid
from datetime import datetime

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class RefreshToken(Base):
  __tablename__ = 'refresh_tokens'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid, primary_key=True, default=uuid.uuid4
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('users.id', ondelete='CASCADE')
  )
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
