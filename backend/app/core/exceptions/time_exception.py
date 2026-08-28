from app.core.exceptions.base_exception import DomainError
from starlette import status


class TimeBoundaryError(DomainError):
  status_code = status.HTTP_400_BAD_REQUEST
  code = 'TIME_BOUNDARY'
  message = 'El bloque se pasa de medianoche'
