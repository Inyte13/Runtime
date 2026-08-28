from app.core.exceptions.base_exception import DomainError
from starlette import status


class InvalidAccessTokenError(DomainError):
  status_code = status.HTTP_401_UNAUTHORIZED
  code = 'INVALID_ACCESS_TOKEN'
  message = 'Access token inválido'


class InvalidRefreshTokenError(DomainError):
  status_code = status.HTTP_401_UNAUTHORIZED
  code = 'INVALID_REFRESH_TOKEN'
  message = 'Refresh token inválido'


class InvalidGoogleTokenError(DomainError):
  status_code = status.HTTP_401_UNAUTHORIZED
  code = 'INVALID_GOOGLE_TOKEN'
  message = 'Token de Google inválido'


class MalformedAccessTokenError(InvalidAccessTokenError):
  code = 'MALFORMED_ACCESS_TOKEN'
  message = 'Access token malformado'


class MissingAccessTokenError(InvalidAccessTokenError):
  code = 'MISSING_ACCESS_TOKEN'
  message = 'No se envió el access token'


class AccessTokenMissingIdError(InvalidAccessTokenError):
  code = 'ACCESS_TOKEN_MISSING_ID'
  message = 'Access token sin id'


class AccessTokenInvalidIdError(InvalidAccessTokenError):
  code = 'ACCESS_TOKEN_INVALID_ID'
  message = 'Access token con id inválido'


class MalformedRefreshTokenError(InvalidRefreshTokenError):
  code = 'MALFORMED_REFRESH_TOKEN'
  message = 'Refresh token malformado'


class ExpiredRefreshTokenError(InvalidRefreshTokenError):
  code = 'EXPIRED_REFRESH_TOKEN'
  message = 'Refresh token expirado'


class MissingRefreshTokenError(InvalidRefreshTokenError):
  code = 'MISSING_REFRESH_TOKEN'
  message = 'No se envió el refresh token'


class GoogleTokenAudienceError(InvalidGoogleTokenError):
  code = 'GOOGLE_TOKEN_INVALID_AUDIENCE'
  message = 'Token de Google no corresponde a esta aplicación'


class GoogleTokenIssuerError(InvalidGoogleTokenError):
  code = 'GOOGLE_TOKEN_INVALID_ISSUER'
  message = 'Emisor del token de Google no es válido'


class GoogleTokenExpiredOrInvalidError(InvalidGoogleTokenError):
  code = 'GOOGLE_TOKEN_EXPIRED_OR_INVALID'
  message = 'Token de Google inválido o expirado'
