from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.bloque_schema import BloqueCreate, BloqueRead, BloqueUpdate
from app.services.bloque_service import (
  actualizar_bloque,
  eliminar_bloque,
  registrar_bloque,
)

bloque_router = APIRouter(tags=['Bloques'])


@bloque_router.get('/bloques/{id}', response_model=BloqueRead)
def get_bloque(session: SessionDep, id: int):
  return buscar_bloque(session, id)


@bloque_router.get('/bloques', response_model=list[BloqueRead])
def get_bloques(
  session: SessionDep,
  fecha: date | None = None,
  inicio: date | None = None,
  final: date | None = None,
):
  if fecha:
    return read_bloques_by_fecha(session, fecha)
  if inicio and final:
    return read_bloques_by_range(session, inicio, final)
  raise HTTPException(
    status_code=400, detail='Debes indicar fecha o inicio/final como parámetros'
  )


@bloque_router.post('/bloques', status_code=201, response_model=BloqueRead)
def post_bloque(session: SessionDep, bloque: BloqueCreate):
  return registrar_bloque(session, bloque)


@bloque_router.patch('/bloques/{id}', response_model=BloqueRead)
def patch_bloque(session: SessionDep, bloque: BloqueUpdate, id: int):
  return actualizar_bloque(session, id, bloque)


@bloque_router.delete('/bloques/{id}', status_code=204)
def delete_bloque(session: SessionDep, id: int):
  eliminar_bloque(session, id)
  return
