from app.api.dependencies import UsuarioDep
from app.core.database import SessionDep
from app.core.exceptions.generic import NotFoundError
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import usuario_service
from fastapi import APIRouter, HTTPException, Response
from starlette import status

router = APIRouter(tags=['Usuarios'], prefix='/usuarios')


@router.patch('/me', response_model=UsuarioResponse)
async def patch(
  session: SessionDep, usuario: UsuarioDep, usuario_update: UsuarioUpdate
):
  try:
    return await usuario_service.actualizar(session, usuario, usuario_update)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def deactivate(
  session: SessionDep, usuario: UsuarioDep, response: Response
):
  await usuario_repository.deactivate(session, usuario)
  response.delete_cookie('access_token')
  response.delete_cookie('id_refresh_token')
