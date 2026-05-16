from datetime import date
import uuid

from sqlalchemy import Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Usuario(Base):
  __tablename__ = 'usuarios'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid, primary_key=True, default=uuid.uuid4
  )
  id_google: Mapped[str] = mapped_column(unique=True, index=True)
  email: Mapped[str] = mapped_column(unique=True, index=True)
  email_verified: Mapped[bool]
  given_name: Mapped[str]
  family_name: Mapped[str]
  picture_url: Mapped[str]
  is_active: Mapped[bool] = mapped_column(default=True)
  create_at: Mapped[date] = mapped_column(default=func.now())