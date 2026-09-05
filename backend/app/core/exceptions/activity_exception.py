from app.core.exceptions.base_exception import DomainError
from starlette import status


class ActivityError(DomainError):
  """Excepción base para activity"""


class DefaultActivityDeletionError(ActivityError):
  status_code = status.HTTP_409_CONFLICT
  code = 'DEFAULT_ACTIVITY_DELETION'
  message = (
    'No se puede eliminar la activity predeterminada antes de establecer otra'
  )


class DefaultActivityMissingError(ActivityError):
  status_code = status.HTTP_409_CONFLICT
  code = 'DEFAULT_ACTIVITY_MISSING'
  message = 'El usuario no tiene una actividad predeterminada configurada'
