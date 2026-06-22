import uuid
from typing import Annotated

from app.core.database import SessionDep
from app.core.exceptions.generic import NotFoundError
from app.core.exceptions.token import (
  InvalidAccessTokenError,
  MalformedAccessTokenError,
)
from app.core.security import validate_access_token
from app.core.settings import settings
from app.models.usuario import Usuario
from app.services.usuario_service import usuario_service
from fastapi import Cookie, Depends, HTTPException
from starlette import status


async def get_usuario(
  session: SessionDep,
  access_token: str | None = Cookie(default=None),
) -> Usuario:
  if not access_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail='No autenticado'
    )

  try:
    payload = validate_access_token(access_token)
  except InvalidAccessTokenError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

  id_str = payload.get('id')
  if not id_str:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token sin id'
    )

  try:
    id_uuid = uuid.UUID(id_str)
    usuario = await usuario_service.buscar(session, id_uuid)
  except (MalformedAccessTokenError, NotFoundError) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

  if not usuario.is_active:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail='Cuenta desactivada'
    )
  return usuario


UsuarioDep = Annotated[Usuario, Depends(get_usuario)]


# Para evitar mandar el usuario completo y solo el id
async def get_current_user_id(usuario: UsuarioDep) -> uuid.UUID:
  return usuario.id


IdUsuarioDep = Annotated[uuid.UUID, Depends(get_current_user_id)]


async def get_admin_usuario(usuario: UsuarioDep) -> Usuario:
  if usuario.email not in settings.ADMIN_EMAILS:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='No tienes permisos de administrador',
    )
  return usuario
