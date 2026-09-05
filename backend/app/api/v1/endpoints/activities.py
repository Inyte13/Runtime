import uuid

from app.api.dependencies import UserDep, UserIdDep
from app.core.database import SessionDep
from app.schemas.activity_schema import (
  ActivityCreate,
  ActivityResponse,
  ActivityResponseDetail,
  ActivityUpdate,
)
from app.services.activity_service import activity_service
from fastapi import APIRouter

router = APIRouter(tags=['Activities'], prefix='/activities')


@router.post('/', status_code=201, response_model=ActivityResponseDetail)
async def post(
  session: SessionDep, user_id: UserIdDep, activity_create: ActivityCreate
):
  return await activity_service.create(session, user_id, activity_create)


@router.patch('/{id}', response_model=ActivityResponse)
async def patch(
  session: SessionDep,
  user_id: UserIdDep,
  activity_update: ActivityUpdate,
  id: uuid.UUID,
):
  return await activity_service.update(session, user_id, activity_update, id)


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, user: UserDep, id: uuid.UUID):
  await activity_service.delete(session, user, id)
