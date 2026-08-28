import uuid

from app.core.database import SessionDep
from app.core.exceptions.token_exception import (
  MissingRefreshTokenError,
)
from app.core.security import set_auth_cookies
from app.schemas.user_schema import UserLoginGoogle, UserResponse
from app.services.access_token_service import access_token_service
from app.services.auth_service import auth_service
from app.services.refresh_token_service import refresh_token_service
from fastapi import APIRouter, Cookie, Response

router = APIRouter(tags=['Auth'], prefix='/auth')


async def _establish_session(
  session: SessionDep, response: Response, user_id: uuid.UUID
) -> None:
  access_token = access_token_service.create({'id': str(user_id)})
  refresh_token = await refresh_token_service.create(session, user_id)
  set_auth_cookies(response, access_token, refresh_token.id)


@router.post(
  '/login',
  response_model=UserResponse,  # Declaramos explicitamente response para setear la cookie
)
async def login(
  session: SessionDep, login_data: UserLoginGoogle, response: Response
):
  user_bd = await auth_service.login(session, login_data.credential)
  await _establish_session(session, response, user_bd.id)
  return user_bd


@router.post('/refresh')
async def refresh(
  session: SessionDep,
  response: Response,
  refresh_token_id: str
  | None = Cookie(  # None, para cambiar el 422 de fastapi a nuestro 401
    default=None
  ),
):
  if refresh_token_id is None:
    raise MissingRefreshTokenError()
  new_access_token, new_refresh_token = await auth_service.refresh(
    session, refresh_token_id
  )
  set_auth_cookies(response, new_access_token, new_refresh_token.id)


@router.post('/reactivate', response_model=UserResponse)
async def reactivate(
  session: SessionDep, login_data: UserLoginGoogle, response: Response
):
  user_bd = await auth_service.reactivate(session, login_data.credential)
  await _establish_session(session, response, user_bd.id)
  return user_bd


@router.post('/logout')
async def logout(
  session: SessionDep,
  response: Response,
  refresh_token_id: str
  | None = Cookie(  # None, para cambiar el 422 de fastapi a nuestro 401
    default=None
  ),
):
  await auth_service.logout(session, refresh_token_id)
  response.delete_cookie('access_token')
  response.delete_cookie('refresh_token_id')
