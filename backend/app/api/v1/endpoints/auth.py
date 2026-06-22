import uuid

from app.core.database import SessionDep
from app.core.exceptions.account import (
  AccountActiveError,
  AccountDeleteError,
  AccountInactiveError,
  AccountRecoverableError,
)
from app.core.exceptions.generic import NotFoundError
from app.core.exceptions.token import (
  ExpiredRefreshTokenError,
  InvalidGoogleTokenError,
  MalformedRefreshTokenError,
)
from app.core.security import crear_access_token, set_auth_cookies
from app.schemas.usuario import UsuarioLoginGoogle, UsuarioResponse
from app.services.auth_service import auth_service
from app.services.refresh_token_service import refresh_token_service
from fastapi import APIRouter, Cookie, HTTPException, Response
from starlette import status

router = APIRouter(tags=['Auth'], prefix='/auth')


async def _iniciar_sesion(
  session: SessionDep, response: Response, id_usuario: uuid.UUID
) -> None:
  access_token = crear_access_token({'id': str(id_usuario)})
  refresh_token = await refresh_token_service.registrar(session, id_usuario)
  set_auth_cookies(response, access_token, refresh_token.id)


@router.post('/login', response_model=UsuarioResponse)
# Declaramos explicitamente response para setear la cookie
async def login(
  session: SessionDep, login_data: UsuarioLoginGoogle, response: Response
):
  try:
    usuario_bd = await auth_service.loguear(session, login_data.credential)
    await _iniciar_sesion(session, response, usuario_bd.id)
    return usuario_bd
  except (InvalidGoogleTokenError, AccountRecoverableError) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except AccountDeleteError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.post('/refresh')
async def refresh(
  session: SessionDep,
  response: Response,
  # None, para cambiar el 422 de fastapi a nuestro 401
  id_refresh_token: str | None = Cookie(default=None),
):
  if not id_refresh_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail='No se envió la cookie'
    )
  try:
    new_access_token, new_refresh_token = await auth_service.refrescar(
      session, id_refresh_token
    )
    set_auth_cookies(response, new_access_token, new_refresh_token.id)
  # No damos mas detalles por seguridad
  except (
    MalformedRefreshTokenError,
    NotFoundError,
    ExpiredRefreshTokenError,
    AccountInactiveError,
  ) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post('/reactivate', response_model=UsuarioResponse)
async def reactivate(
  session: SessionDep, login_data: UsuarioLoginGoogle, response: Response
):
  try:
    usuario_bd = await auth_service.reactivar(session, login_data.credential)
    await _iniciar_sesion(session, response, usuario_bd.id)
    return usuario_bd
  except (
    InvalidGoogleTokenError,
    NotFoundError,
  ) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except AccountActiveError as e:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
  except AccountDeleteError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post('/logout')
async def logout(
  session: SessionDep,
  response: Response,
  id_refresh_token: str | None = Cookie(default=None),
):
  try:
    await auth_service.desloguear(session, id_refresh_token)
    response.delete_cookie('access_token')
    response.delete_cookie('id_refresh_token')
  except (
    MalformedRefreshTokenError,
    NotFoundError,
    ExpiredRefreshTokenError,
  ) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
