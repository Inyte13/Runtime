import uuid

from app.api.dependencies import UserIdDep
from app.core.database import PathDate, QueryDate, SessionDep
from app.schemas.block_schema import BlockResponse
from app.schemas.day_schema import (
  DayCalendar,
  DayResponse,
  DayResponseDetail,
  DayUpdate,
)
from app.services.block_service import block_service
from app.services.day_service import day_service
from fastapi import APIRouter, Body

router = APIRouter(tags=['Days'], prefix='/days')


@router.get('/{date}', response_model=DayResponseDetail)
async def get(session: SessionDep, user_id: UserIdDep, date: PathDate):
  return await day_service.get_with_blocks(session, user_id, date)


@router.get('/', response_model=list[DayCalendar])
async def get_resumen(
  session: SessionDep,
  user_id: UserIdDep,
  date_from: QueryDate,
  date_to: QueryDate,
):
  return await day_service.get_calendar_by_range(
    session, user_id, date_from, date_to
  )


@router.patch('/{date}', response_model=DayResponse)
async def upsert(
  session: SessionDep, user_id: UserIdDep, day: DayUpdate, date: PathDate
):
  return await day_service.upsert(session, user_id, day, date)


@router.patch('/{date}/reorder', response_model=list[BlockResponse])
async def reorder(
  session: SessionDep,
  user_id: UserIdDep,
  date: PathDate,
  block_ids: list[uuid.UUID] = Body(...),
):
  return await block_service.reorder(session, user_id, date, block_ids)


@router.delete('/{date}', status_code=204)
async def delete(session: SessionDep, user_id: UserIdDep, date: PathDate):
  await day_service.delete(session, user_id, date)
