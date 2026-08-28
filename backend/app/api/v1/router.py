from app.api.v1.endpoints import (
  activities,
  admin,
  auth,
  blocks,
  categories,
  days,
  users,
)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(admin.router)
api_router.include_router(users.router)
api_router.include_router(activities.router)
api_router.include_router(categories.router)
api_router.include_router(blocks.router)
api_router.include_router(days.router)
