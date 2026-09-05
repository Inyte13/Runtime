from app.core.exceptions.base_exception import DomainError
from starlette import status


class BlockError(DomainError):
  """Excepción base para block"""


class BlockDateMismatchError(BlockError):
  status_code = status.HTTP_400_BAD_REQUEST
  code = 'BLOCK_DATE_MISMATCH'
  message = 'El bloque objetivo no pertenece a la fecha indicada'
