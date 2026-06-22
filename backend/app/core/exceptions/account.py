class AccountError(Exception):
  """Excepción base para estados especiales de la cuenta"""


class AccountRecoverableError(AccountError):
  def __init__(self, detail: str = 'cuenta_recuperable'):
    super().__init__(detail)


class AccountDeleteError(AccountError):
  def __init__(
    self, detail: str = 'Cuenta eliminada, regístrese de nuevo'
  ):
    super().__init__(detail)


class AccountInactiveError(AccountError):
  def __init__(self, detail: str = 'Cuenta desactivada'):
    super().__init__(detail)


class AccountActiveError(AccountError):
  def __init__(self, detail: str = 'Cuenta activa'):
    super().__init__(detail)
