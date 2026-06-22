class InvalidAccessTokenError(Exception):
  pass


class InvalidRefreshTokenError(Exception):
  pass


class InvalidGoogleTokenError(Exception):
  pass


class MalformedAccessTokenError(InvalidAccessTokenError):
  def __init__(self, detail: str = 'Access token inválido'):
    super().__init__(detail)


class MalformedRefreshTokenError(InvalidRefreshTokenError):
  def __init__(self, detail: str = 'Refresh token inválido'):
    super().__init__(detail)


class ExpiredRefreshTokenError(InvalidRefreshTokenError):
  def __init__(self, detail: str = 'Refresh token expirado'):
    super().__init__(detail)


class GoogleTokenAudienceError(InvalidGoogleTokenError):
  def __init__(
    self, detail: str = 'Token de Google no corresponde a esta aplicación'
  ):
    super().__init__(detail)


class GoogleTokenIssuerError(InvalidGoogleTokenError):
  def __init__(self, detail: str = 'Emisor del token de Google no es válido'):
    super().__init__(detail)


class GoogleTokenExpiredOrInvalidError(InvalidGoogleTokenError):
  def __init__(self, detail: str = 'Token de Google inválido o expirado'):
    super().__init__(detail)
