from app.api.dependencies import get_admin_user
from app.core.database import SessionDep
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import UserResponse
from fastapi import APIRouter, Depends

router = APIRouter(
  tags=['Admin'], prefix='/admin', dependencies=[Depends(get_admin_user)]
)


# list en lugar de Sequence porque es un JSON Array
@router.get('/users', response_model=list[UserResponse])
async def get_users(session: SessionDep):
  return await user_repository.get_all(session)
