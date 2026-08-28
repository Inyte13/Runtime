from app.core.exceptions.base_exception import DomainError
from starlette import status


class NotFoundError(DomainError):
  status_code = 404
  code = 'NOT_FOUND'
  message = 'No se encontró'


class ConflictError(DomainError):
  status_code = 409
  code = 'CONFLICT'
  message = 'Ocurrió un conflicto'


class InvalidDateRangeError(DomainError):
  status_code = status.HTTP_400_BAD_REQUEST
  code = 'INVALID_DATE_RANGE'
  message = 'Fecha inválida'
