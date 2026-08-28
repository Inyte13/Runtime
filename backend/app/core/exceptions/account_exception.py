from app.core.exceptions.base_exception import DomainError
from starlette import status


class AccountError(DomainError):
  """Excepción base para estados especiales de la cuenta"""


class AccountRecoverableError(AccountError):
  status_code = status.HTTP_401_UNAUTHORIZED
  code = 'ACCOUNT_RECOVERABLE'
  message = 'La cuenta puede recuperarse'


class AccountDeleteError(AccountError):
  status_code = 404
  code = 'ACCOUNT_DELETED'
  message = 'Cuenta eliminada, regístrese de nuevo'


class AccountInactiveError(AccountError):
  status_code = status.HTTP_401_UNAUTHORIZED
  code = 'ACCOUNT_INACTIVE'
  message = 'Cuenta desactivada'


class AccountActiveError(AccountError):
  status_code = status.HTTP_409_CONFLICT
  code = 'ACCOUNT_ALREADY_ACTIVE'
  message = 'Cuenta activa'


class AdminPermissionRequiredError(DomainError):
  status_code = status.HTTP_403_FORBIDDEN
  code = 'ADMIN_PERMISSION_REQUIRED'
  message = 'No tienes permisos de administrador'
