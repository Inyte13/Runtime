class DomainError(Exception):
  status_code = 500
  code = 'INTERNAL_ERROR'
  message = 'Ocurrió un error inesperado'

  def __init__(self, message: str | None = None):
    self.message = message or self.message
    # Reemplazamos el message del padre Exception
    super().__init__(self.message)
