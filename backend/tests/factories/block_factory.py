from datetime import date

from app.core.constants import GRANULARITY_HOURS
from app.models.block import Block
from app.models.user import User
from app.schemas.block_schema import BlockCreate, EdgePosition, RelativePosition
from app.services.block_service import block_service
from sqlalchemy.ext.asyncio import AsyncSession


async def create_block(
  session: AsyncSession,
  user: User,
  date: date,
  placement: EdgePosition | RelativePosition = EdgePosition(position='end'),
  duration: float = GRANULARITY_HOURS,
  description: str | None = None,
) -> Block:
  return await block_service.create(
    session,
    user,
    BlockCreate(
      date=date,
      duration=duration,
      description=description,
      placement=placement,
    ),
  )


async def create_blocks(
  session: AsyncSession,
  user: User,
  date: date,
  count: int = 2,
  duration: float = GRANULARITY_HOURS,
  description: str | None = None,
  overrides_duration: dict[int, float] | None = None,
  overrides_description: dict[int, str | None] | None = None,
) -> list[Block]:
  overrides_duration = {} if overrides_duration is None else overrides_duration
  overrides_description = (
    {} if overrides_description is None else overrides_description
  )
  blocks: list[Block] = []
  for block_index in range(count):
    block_duration = overrides_duration.get(block_index, duration)
    block_description = overrides_description.get(block_index, description)
    block_create = await create_block(
      session,
      user,
      date,
      duration=block_duration,
      description=block_description,
    )
    blocks.append(block_create)
  return blocks
