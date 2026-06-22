import httpx
from app.core.exceptions.token import (
  GoogleTokenAudienceError,
  GoogleTokenExpiredOrInvalidError,
  GoogleTokenIssuerError,
)
from app.core.settings import settings
from pydantic import BaseModel


class DataGoogle(BaseModel):
  id_google: str
  email: str
  email_verified: bool
  given_name: str | None = None
  family_name: str | None = None
  picture_url: str | None = None


async def verificar_google_token(credential: str) -> DataGoogle:
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
    if payload.get('aud') != settings.GOOGLE_CLIENT_ID:
      raise GoogleTokenAudienceError()
    # Validar que sea google (emisor/issuer)
    if payload.get('iss') not in [
      'accounts.google.com',
      'https://accounts.google.com',
    ]:
      raise GoogleTokenIssuerError()
    # Cuando usamos [] si falla explota, si usamos .get y no esta nos da none
    return DataGoogle(
      id_google=payload['sub'],
      email=payload['email'],
      email_verified=payload.get('email_verified', False),
      given_name=payload.get('given_name'),
      family_name=payload.get('family_name'),
      picture_url=payload.get('picture'),
    )
