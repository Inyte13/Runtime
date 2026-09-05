from app.core.exceptions.base_exception import DomainError
from starlette import status


class CategoryError(DomainError):
  """Excepción base para category"""


class DefaultCategoryDeletionError(CategoryError):
  status_code = status.HTTP_409_CONFLICT
  code = 'DEFAULT_CATEGORY_DELETION'
  message = (
    'No se puede eliminar la categoría predeterminada antes de establecer otra'
  )
