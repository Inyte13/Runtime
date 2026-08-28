import uuid

from app.models.activity import Activity
from app.models.block import Block
from app.repositories.base_repository import BaseRepository
from app.schemas.activity_schema import ActivityUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActivityRepository(BaseRepository[Activity, ActivityUpdate]):
  async def is_deletable(self, session: AsyncSession, id: uuid.UUID) -> bool:
    statement = select(select(Block.id).where(Block.activity_id == id).exists())
    result = await session.execute(statement)
    return not bool(result.scalar())

  async def get_is_deletable_map(
    self, session: AsyncSession, activities_ids: list[uuid.UUID]
  ) -> dict[uuid.UUID, bool]:
    if not activities_ids:
      return {}
    statement = (
      select(Block.activity_id)
      .where(Block.activity_id.in_(activities_ids))
      .distinct()
    )
    result = await session.execute(statement)
    # Solo guardamos True, porque cuando lo usemos indicaremos default False
    is_deletable_map: dict[uuid.UUID, bool] = {}
    for activity_id in result.scalars().all():
      is_deletable_map[activity_id] = True
    return is_deletable_map


activity_repository = ActivityRepository(Activity)
