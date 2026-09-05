import uuid
from collections.abc import Sequence

from app.models.activity import Activity
from app.models.block import Block
from app.repositories.base_repository import BaseRepository
from app.schemas.activity_schema import ActivityUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ActivityRepository(BaseRepository[Activity, ActivityUpdate]):
  async def get_all(
    self, session: AsyncSession, user_id: uuid.UUID
  ) -> Sequence[Activity]:
    statement = (
      select(Activity)
      .where(Activity.user_id == user_id)
      .order_by(Activity.name)
    )
    result = await session.execute(statement)
    return result.scalars().all()

  async def is_deletable(self, session: AsyncSession, id: uuid.UUID) -> bool:
    statement = select(select(Block.id).where(Block.activity_id == id).exists())
    result = await session.execute(statement)
    return not bool(result.scalar())

  async def get_is_deletable_map(
    self, session: AsyncSession, activities_ids: list[uuid.UUID]
  ) -> dict[uuid.UUID, bool]:
    if activities_ids == []:
      return {}
    statement = (
      select(Block.activity_id)
      .where(Block.activity_id.in_(activities_ids))
      .distinct()
    )
    result = await session.execute(statement)
    # Solo guardamos False, porque cuando lo usemos indicaremos default True
    is_deletable_map: dict[uuid.UUID, bool] = {}
    for activity_id in result.scalars().all():
      is_deletable_map[activity_id] = False
    return is_deletable_map


activity_repository = ActivityRepository(Activity)
