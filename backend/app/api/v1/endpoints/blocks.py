import uuid

from app.api.dependencies import UserDep, UserIdDep
from app.core.database import SessionDep
from app.schemas.block_schema import BlockCreate, BlockResponse, BlockUpdate
from app.services.block_service import block_service
from fastapi import APIRouter

router = APIRouter(tags=['Blocks'], prefix='/blocks')

# TODO: Un get para traer los blocks para las estadisticas


@router.post('/', status_code=201, response_model=BlockResponse)
async def post(session: SessionDep, user: UserDep, block_create: BlockCreate):
  return await block_service.create(session, user, block_create)


@router.patch('/{id}', response_model=BlockResponse)
async def patch(
  session: SessionDep,
  user_id: UserIdDep,
  block_update: BlockUpdate,
  id: uuid.UUID,
):
  return await block_service.update(session, user_id, block_update, id)


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, user_id: UserIdDep, id: uuid.UUID):
  await block_service.delete(session, user_id, id)
