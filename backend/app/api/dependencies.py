import uuid
from typing import Annotated

from app.core.database import SessionDep
from app.core.exceptions.account_exception import (
  AccountInactiveError,
  AdminPermissionRequiredError,
)
from app.core.exceptions.token_exception import (
  AccessTokenInvalidIdError,
  AccessTokenMissingIdError,
  MissingAccessTokenError,
)
from app.core.settings import get_settings
from app.models.user import User
from app.services.access_token_service import access_token_service
from app.services.user_service import user_service
from fastapi import Cookie, Depends


async def get_user(
  session: SessionDep,
  access_token: str | None = Cookie(default=None),
) -> User:
  if access_token is None:
    raise MissingAccessTokenError()
  payload = access_token_service.validate(access_token)

  id_value = payload.get('id')
  if id_value is None:
    raise AccessTokenMissingIdError()
  if not isinstance(id_value, str):
    raise AccessTokenInvalidIdError()
  try:
    id_uuid = uuid.UUID(id_value)
  except ValueError:
    raise AccessTokenInvalidIdError()
  user_bd = await user_service.get(session, id_uuid)

  if user_bd.is_active is False:
    raise AccountInactiveError()
  return user_bd


UserDep = Annotated[User, Depends(get_user)]


# Para evitar mandar el user completo y solo el id
async def get_user_id(user: UserDep) -> uuid.UUID:
  return user.id


UserIdDep = Annotated[uuid.UUID, Depends(get_user_id)]


async def get_admin_user(user: UserDep) -> User:
  if user.email not in get_settings().ADMIN_EMAILS:
    raise AdminPermissionRequiredError()
  return user
