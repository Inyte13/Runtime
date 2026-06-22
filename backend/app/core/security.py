import uuid
from datetime import datetime, timedelta, timezone

# Any, para que pueda ser datetime
from typing import Any

from app.core.exceptions.token import InvalidAccessTokenError
from app.core.settings import settings
from fastapi import Response
from jose import JWTError, jwt


def crear_access_token(data: dict[str, Any]) -> str:
  payload = data.copy()
  payload['exp'] = datetime.now(timezone.utc) + timedelta(
    minutes=settings.ACCESS_TOKEN_DURATION_MINUTES
  )
  return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def validate_access_token(token: str) -> dict[str, Any]:
  try:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
  except JWTError:
    raise InvalidAccessTokenError()


# Si ya hay una cookie, la sobreescribe
def set_auth_cookies(
  response: Response, access_token: str, id_refresh_token: uuid.UUID
):
  response.set_cookie(
    key='access_token',
    value=access_token,
    httponly=True,
    secure=settings.PRODUCTION,
    max_age=settings.ACCESS_TOKEN_DURATION_MINUTES * 60,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
  response.set_cookie(
    key='id_refresh_token',
    value=str(id_refresh_token),
    httponly=True,
    secure=settings.PRODUCTION,
    max_age=settings.REFRESH_TOKEN_DURATION_DAYS * 86400,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
