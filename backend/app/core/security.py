import uuid

from app.core.settings import get_settings
from fastapi import Response


# Si ya hay una cookie, la sobreescribe
def set_auth_cookies(
  response: Response, access_token: str, refresh_token_id: uuid.UUID
):
  response.set_cookie(
    key='access_token',
    value=access_token,
    httponly=True,
    secure=get_settings().PRODUCTION,
    max_age=get_settings().ACCESS_TOKEN_DURATION_MINUTES * 60,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
  response.set_cookie(
    key='refresh_token_id',
    value=str(refresh_token_id),
    httponly=True,
    secure=get_settings().PRODUCTION,
    max_age=get_settings().REFRESH_TOKEN_DURATION_DAYS * 86400,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
