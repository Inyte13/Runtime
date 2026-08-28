import uuid

from app.api.dependencies import UserIdDep
from app.core.database import SessionDep
from app.schemas.category_schema import (
  CategoryCreate,
  CategoryResponse,
  CategoryResponseDetail,
  CategoryUpdate,
)
from app.services.category_service import category_service
from fastapi import APIRouter

router = APIRouter(tags=['Categories'], prefix='/categories')


@router.get('/', response_model=list[CategoryResponseDetail])
async def get_all(session: SessionDep, user_id: UserIdDep):
  return await category_service.get_all_with_activities(session, user_id)


@router.post('/', status_code=201, response_model=CategoryResponse)
async def post(
  session: SessionDep, category_create: CategoryCreate, user_id: UserIdDep
):
  return await category_service.create(session, category_create, user_id)


@router.patch('/{id}', response_model=CategoryResponse)
async def patch(
  session: SessionDep,
  user_id: UserIdDep,
  category_update: CategoryUpdate,
  id: uuid.UUID,
):
  return await category_service.update(session, user_id, category_update, id)


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, user_id: UserIdDep, id: uuid.UUID):
  await category_service.delete(session, user_id, id)
