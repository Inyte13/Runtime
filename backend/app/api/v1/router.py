from app.api.v1.endpoints import (
  actividades,
  admin,
  auth,
  bloques,
  categorias,
  dias,
  usuarios,
)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(admin.router)
api_router.include_router(usuarios.router)
api_router.include_router(actividades.router)
api_router.include_router(categorias.router)
api_router.include_router(bloques.router)
api_router.include_router(dias.router)
