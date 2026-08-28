from app.api.dependencies import UserDep
from app.core.database import SessionDep
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import UserResponse, UserUpdate
from app.services.user_service import user_service
from fastapi import APIRouter, Response
from starlette import status

router = APIRouter(tags=['Users'], prefix='/users')


@router.patch('/me', response_model=UserResponse)
async def patch(session: SessionDep, user: UserDep, user_update: UserUpdate):
  return await user_service.update(session, user, user_update)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def deactivate(session: SessionDep, user: UserDep, response: Response):
  await user_repository.deactivate(session, user)
  response.delete_cookie('access_token')
  response.delete_cookie('refresh_token_id')
