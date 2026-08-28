import httpx
from app.core.exceptions.token_exception import (
  GoogleTokenAudienceError,
  GoogleTokenExpiredOrInvalidError,
  GoogleTokenIssuerError,
)
from app.core.settings import get_settings
from pydantic import BaseModel, ValidationError


class GoogleUserData(BaseModel):
  google_id: str
  email: str
  email_verified: bool
  given_name: str | None = None
  family_name: str | None = None
  picture_url: str | None = None


async def verificar_google_token(credential: str) -> GoogleUserData:
  # Abrimos una conexión http
  async with httpx.AsyncClient() as client:
    response = await client.get(
      'https://oauth2.googleapis.com/tokeninfo',
      params={'id_token': credential},
    )
    if response.status_code != 200:
      raise GoogleTokenExpiredOrInvalidError()
    payload = response.json()

    # Validar que el token corresponda a nuestro Client ID (audiencia)
    if payload.get('aud') != get_settings().GOOGLE_CLIENT_ID:
      raise GoogleTokenAudienceError()

    # Validar que sea google (emisor/issuer)
    if payload.get('iss') not in [
      'accounts.google.com',
      'https://accounts.google.com',
    ]:
      raise GoogleTokenIssuerError()

    google_id = payload.get('sub')
    email = payload.get('email')

    if not google_id or not email:
      raise GoogleTokenExpiredOrInvalidError()
    # Cuando usamos [] si falla explota, si usamos .get y no está, nos da none
    try:
      return GoogleUserData(
        google_id=google_id,
        email=email,
        email_verified=payload.get('email_verified', False),
        given_name=payload.get('given_name'),
        family_name=payload.get('family_name'),
        picture_url=payload.get('picture'),
      )
    except ValidationError:
      raise GoogleTokenExpiredOrInvalidError()
