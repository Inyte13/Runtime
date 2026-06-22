import uuid

from app.api.dependencies import IdUsuarioDep
from app.core.database import SessionDep
from app.core.exceptions.generic import ConflictError, NotFoundError
from app.schemas.categoria import (
  CategoriaCreate,
  CategoriaResponse,
  CategoriaResponseDetail,
  CategoriaUpdate,
)
from app.services.categoria_service import categoria_service
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

router = APIRouter(tags=['Categorias'], prefix='/categorias')


@router.get('/', response_model=list[CategoriaResponseDetail])
async def get_all(session: SessionDep, id_usuario: IdUsuarioDep):
  return await categoria_service.mostrar_todas(session, id_usuario)


@router.post('/', status_code=201, response_model=CategoriaResponseDetail)
async def post(
  session: SessionDep, categoria: CategoriaCreate, id_usuario: IdUsuarioDep
):
  try:
    return await categoria_service.registrar(session, categoria, id_usuario)
  # Usando el unique del schema
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )


@router.patch('/{id}', response_model=CategoriaResponse)
async def patch(
  session: SessionDep,
  id_usuario: IdUsuarioDep,
  categoria: CategoriaUpdate,
  id: uuid.UUID,
):
  try:
    return await categoria_service.actualizar(
      session, id_usuario, categoria, id
    )
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  # Usando el unique del schema
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre ya existe'
    )


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, id_usuario: IdUsuarioDep, id: uuid.UUID):
  try:
    await categoria_service.eliminar(session, id_usuario, id)
  except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ConflictError as e:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
