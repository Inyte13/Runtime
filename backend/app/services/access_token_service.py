from datetime import datetime, timedelta, timezone

# Any, para que pueda ser datetime
from typing import Any

from app.core.constants import JWT_ALGORITHM
from app.core.exceptions.token_exception import InvalidAccessTokenError
from app.core.settings import get_settings
from jose import JWTError, jwt


class AccessTokenService:
  def create(
    self, data: dict[str, Any]
  ) -> str:  # Any porque 'exp': datetime...
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(
      minutes=get_settings().ACCESS_TOKEN_DURATION_MINUTES
    )
    return jwt.encode(
      payload, get_settings().SECRET_KEY, algorithm=JWT_ALGORITHM
    )

  def validate(self, token: str) -> dict[str, Any]:
    try:
      return jwt.decode(
        token, get_settings().SECRET_KEY, algorithms=[JWT_ALGORITHM]
      )
    except JWTError:
      raise InvalidAccessTokenError()


access_token_service = AccessTokenService()
