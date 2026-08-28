import uuid
from datetime import date, datetime

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
  __tablename__ = 'users'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid, primary_key=True, default=uuid.uuid4
  )
  google_id: Mapped[str] = mapped_column(unique=True, index=True)
  email: Mapped[str] = mapped_column(unique=True, index=True)
  email_verified: Mapped[bool]
  given_name: Mapped[str | None]
  family_name: Mapped[str | None]
  picture_url: Mapped[str | None]
  is_active: Mapped[bool] = mapped_column(default=True)
  created_at: Mapped[date] = mapped_column(server_default=func.now())
  deactivated_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), default=None
  )

  # Solo es none para la bd, pero después controlamos
  activity_default_id: Mapped[uuid.UUID | None] = mapped_column(
    ForeignKey(
      'activities.id',
      name='fk_user_activity_default',
      ondelete='RESTRICT',  # Para que no pueda delete una actividad que se use en este campo
      use_alter=True,  # Para solucionar las relaciones circulares
    )
  )
