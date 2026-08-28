from uuid import uuid4

from app.models.user import User
from app.services.user_service import user_service
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.google import GoogleUserData


async def create_user(
  session: AsyncSession,
  *,  # Hace que los params siguientes sean nombrados explícitamente
  google_id: str | None = None,
  email: str | None = None,
  email_verified: bool = True,
  given_name: str = 'Test',
  family_name: str = 'User',
  picture_url: str | None = None,
) -> User:
  unique_id = uuid4().hex
  google_user_data = GoogleUserData(
    google_id=google_id or f'google-{unique_id}',
    email=email or f'test-{unique_id}@example.com',
    email_verified=email_verified,
    given_name=given_name,
    family_name=family_name,
    picture_url=picture_url,
  )

  return await user_service.create(session, google_user_data)
