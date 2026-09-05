import uuid

from app.api.dependencies import UserIdDep
from app.core.database import SessionDep
from app.schemas.hidden_activity_schema import (
  HiddenActivityCreate,
  HiddenActivityResponse,
)
from app.services.hidden_activity_service import hidden_activity_service
from fastapi import APIRouter

router = APIRouter(tags=['Hidden Activities'], prefix='/hidden-activities')


@router.post('/', status_code=201, response_model=HiddenActivityResponse)
async def post(
  session: SessionDep,
  user_id: UserIdDep,
  hidden_activity_create: HiddenActivityCreate,
):
  return await hidden_activity_service.create(
    session, user_id, hidden_activity_create
  )


@router.delete('/{id}', status_code=204)
async def delete(session: SessionDep, user_id: UserIdDep, id: uuid.UUID):
  await hidden_activity_service.delete(session, user_id, id)
