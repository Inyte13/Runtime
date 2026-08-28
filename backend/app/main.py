import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.router import api_router
from app.core.database import Base, engine
from app.core.exceptions.base_exception import DomainError
from app.core.exceptions.generic_exception import ConflictError
from app.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Application lifespan events"""
  # Startup
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield
  # Shutdown


app = FastAPI(
  title='Runtime App',
  version='1.0.0',
  lifespan=lifespan,
)


@app.exception_handler(DomainError)
async def handle_domain_error(request: Request, error: DomainError):
  return JSONResponse(
    status_code=error.status_code,
    content={
      'code': error.code,
      'message': error.message,
    },
  )


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, error: IntegrityError):
  return await handle_domain_error(request, ConflictError())


# Errores en consola
logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def handle_exception_error(request: Request, error: Exception):
  # Errores en consola
  logger.exception(
    'Unhandled exception: %s %s',
    request.method,
    request.url.path,
  )

  return await handle_domain_error(request, DomainError())


# CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=get_settings().CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Include routers
app.include_router(api_router, prefix='/api/v1')

if __name__ == '__main__':
  import uvicorn

  uvicorn.run('app.main:app', reload=True, port=get_settings().PORT)
