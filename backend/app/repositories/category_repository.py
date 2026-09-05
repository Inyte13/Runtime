import uuid
from collections.abc import Sequence

from app.models.activity import Activity
from app.models.block import Block
from app.models.category import Category
from app.repositories.base_repository import BaseRepository
from app.schemas.category_schema import CategoryUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository(BaseRepository[Category, CategoryUpdate]):
  async def is_deletable(self, session: AsyncSession, id: uuid.UUID) -> bool:
    statement = (
      select(Activity.id)
      .join(Block, Block.activity_id == Activity.id)
      .where(Activity.category_id == id)
      .limit(1)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is None

  async def get_all(
    self, session: AsyncSession, user_id: uuid.UUID
  ) -> Sequence[Category]:
    statement = (
      select(Category)
      .where(Category.user_id == user_id)
      .order_by(Category.name)
    )
    result = await session.execute(statement)
    return result.scalars().all()


category_repository = CategoryRepository(Category)
