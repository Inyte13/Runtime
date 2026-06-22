from app.api.dependencies import get_admin_usuario
from app.core.database import SessionDep
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioResponse
from fastapi import APIRouter, Depends

router = APIRouter(
  tags=['Admin'], prefix='/admin', dependencies=[Depends(get_admin_usuario)]
)


# list en lugar de Sequence porque es un JSON Array
@router.get('/usuarios', response_model=list[UsuarioResponse])
async def get_usuarios(session: SessionDep):
  return await usuario_repository.get_all(session)
