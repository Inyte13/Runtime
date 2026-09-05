import uuid
from datetime import date, time

from app.core.exceptions.activity_exception import DefaultActivityMissingError
from app.core.exceptions.block_exception import BlockDateMismatchError
from app.core.exceptions.generic_exception import ConflictError
from app.core.exceptions.time_exception import TimeBoundaryError
from app.models.block import Block
from app.models.user import User
from app.repositories.activity_repository import activity_repository
from app.repositories.block_repository import block_repository
from app.schemas.block_schema import BlockCreate, BlockUpdate, RelativePosition
from app.services.base_service import get_or_raise
from app.services.day_service import day_service
from app.utils.hours import (
  calculate_hour_end,
  hour_end_to_minutes,
  minutes_to_hours,
  recalculate_hours,
)
from sqlalchemy.ext.asyncio import AsyncSession

# TODO: Solucionar dos peticiones al mismo tiempo

class BlockService:
  def __init__(self):
    self.repository = block_repository

  async def create(
    self, session: AsyncSession, user: User, block_create: BlockCreate
  ) -> Block:
    if user.default_activity_id is None:
      raise DefaultActivityMissingError('User no tiene default activity')
    await day_service.get_or_create(session, block_create.date, user.id)
    if block_create.placement.position == 'end':
      return await self._create_end(
        session, block_create, user.id, user.default_activity_id
      )
    if block_create.placement.position == 'after':
      return await self._create_after(
        session, block_create, user.id, user.default_activity_id
      )
    if block_create.placement.position == 'before':
      return await self._create_before(
        session, block_create, user.id, user.default_activity_id
      )
    raise ValueError(f'Position {block_create.placement.position} no declarada')

  async def _create_end(
    self,
    session: AsyncSession,
    block_create: BlockCreate,
    user_id: uuid.UUID,
    activity_id: uuid.UUID,
  ) -> Block:
    last_block = await self.repository.get_last(
      session, block_create.date, user_id
    )
    if last_block is None:
      hour = time(0, 0)
    elif hour_end_to_minutes(last_block.hour_end) >= 1440:
      raise TimeBoundaryError()
    else:
      hour = last_block.hour_end
    new_block = Block(
      user_id=user_id,
      date=block_create.date,
      hour=hour,
      hour_end=calculate_hour_end(hour, block_create.duration),
      duration=block_create.duration,
      description=block_create.description,
      activity_id=activity_id,
    )
    return await self.repository.create(session, new_block)

  async def _create_after(
    self,
    session: AsyncSession,
    block_create: BlockCreate,
    user_id: uuid.UUID,
    activity_id: uuid.UUID,
  ) -> Block:
    assert isinstance(block_create.placement, RelativePosition)
    target_block = await get_or_raise(
      session, self.repository, block_create.placement.target_id, user_id
    )
    if target_block.date != block_create.date:
      raise BlockDateMismatchError()
    last_block = await self.repository.get_last(
      session, block_create.date, user_id
    )
    assert last_block is not None
    if target_block.id == last_block.id:
      if hour_end_to_minutes(last_block.hour_end) >= 1440:
        raise TimeBoundaryError()

      new_block = Block(
        user_id=user_id,
        date=block_create.date,
        hour=last_block.hour_end,
        hour_end=calculate_hour_end(last_block.hour_end, block_create.duration),
        duration=block_create.duration,
        description=block_create.description,
        activity_id=activity_id,
      )
      return await self.repository.create(session, new_block)
    affected_blocks = await self.repository.get_by_range(
      session,
      block_create.date,
      user_id,
      hour_from=target_block.hour,
      exclude_hour_from=True,
    )
    recalculate_hours(affected_blocks, block_create.duration)
    new_block = Block(
      user_id=user_id,
      date=block_create.date,
      hour=target_block.hour_end,
      hour_end=calculate_hour_end(target_block.hour_end, block_create.duration),
      duration=block_create.duration,
      description=block_create.description,
      activity_id=activity_id,
    )
    return await self.repository.create(session, new_block)

  async def _create_before(
    self,
    session: AsyncSession,
    block_create: BlockCreate,
    user_id: uuid.UUID,
    activity_id: uuid.UUID,
  ) -> Block:
    assert isinstance(block_create.placement, RelativePosition)
    target_block = await get_or_raise(
      session, self.repository, block_create.placement.target_id, user_id
    )
    if target_block.date != block_create.date:
      raise BlockDateMismatchError()
    new_block = Block(
      user_id=user_id,
      date=block_create.date,
      hour=target_block.hour,
      hour_end=calculate_hour_end(target_block.hour, block_create.duration),
      duration=block_create.duration,
      description=block_create.description,
      activity_id=activity_id,
    )
    affected_blocks = await self.repository.get_by_range(
      session, block_create.date, user_id, hour_from=target_block.hour
    )
    recalculate_hours(affected_blocks, block_create.duration)
    return await self.repository.create(session, new_block)

  async def reorder(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    date: date,
    blocks_ids: list[uuid.UUID],
  ) -> list[Block]:
    blocks = await block_repository.get_by_range(session, date, user_id)
    blocks_dict: dict[uuid.UUID, Block] = {}
    blocks_ids_bd: list[uuid.UUID] = []
    for block in blocks:
      blocks_ids_bd.append(block.id)
      blocks_dict[block.id] = block
    if blocks_ids == blocks_ids_bd:
      return list(blocks)
    # set porque no importa el orden, solo los mismos elementos
    if len(blocks_ids) != len(blocks) or set(blocks_ids) != blocks_dict.keys():
      raise ConflictError('Los bloques no coinciden')
    minutes_temp = 0
    updated_blocks: list[Block] = []
    for block_id in blocks_ids:
      block = blocks_dict[block_id]
      block.hour = minutes_to_hours(minutes_temp)
      minutes_temp += int(block.duration * 60)
      block.hour_end = minutes_to_hours(minutes_temp)
      updated_blocks.append(block)
    return updated_blocks

  async def update(
    self,
    session: AsyncSession,
    user_id: uuid.UUID,
    block_update: BlockUpdate,
    id: uuid.UUID,
  ) -> Block:
    block_bd = await get_or_raise(session, self.repository, id, user_id)
    if block_update.activity_id is not None:
      await get_or_raise(
        session, activity_repository, block_update.activity_id, user_id
      )
    if (
      block_update.duration is None
      or block_update.duration == block_bd.duration
    ):
      return await self.repository.update(session, block_bd, block_update)
    affected_blocks = await self.repository.get_by_range(
      session,
      block_bd.date,
      user_id,
      hour_from=block_bd.hour,
      exclude_hour_from=True,
    )
    if len(affected_blocks) > 0:
      recalculate_hours(
        affected_blocks, block_update.duration - block_bd.duration
      )
    block_bd.duration = block_update.duration
    block_bd.hour_end = calculate_hour_end(block_bd.hour, block_update.duration)
    return await self.repository.update(session, block_bd, block_update)

  async def delete(
    self, session: AsyncSession, user_id: uuid.UUID, id: uuid.UUID
  ) -> None:
    block_bd = await get_or_raise(session, self.repository, id, user_id)
    affected_blocks = await self.repository.get_by_range(
      session,
      block_bd.date,
      user_id,
      hour_from=block_bd.hour,
      exclude_hour_from=True,
    )
    if len(affected_blocks) > 0:
      recalculate_hours(affected_blocks, -block_bd.duration)
    await self.repository.delete(session, block_bd)


block_service = BlockService()
