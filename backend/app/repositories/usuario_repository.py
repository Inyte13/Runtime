import uuid
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import override

from app.models.usuario import Usuario
from app.repositories.base_respository import BaseRepository
from app.schemas.usuario import UsuarioUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioRepository(BaseRepository[Usuario, UsuarioUpdate]):
  @override
  async def get(  # type: ignore
    self, session: AsyncSession, id: uuid.UUID
  ) -> Usuario | None:
    return await session.get(Usuario, id)

  async def get_all(self, session: AsyncSession) -> Sequence[Usuario]:
    result = await session.execute(select(Usuario))
    return result.scalars().all()

  async def get_by_google(
    self, session: AsyncSession, id_google: str
  ) -> Usuario | None:
    statement = select(Usuario).where(Usuario.id_google == id_google)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

  async def deactivate(
    self, session: AsyncSession, usuario: Usuario
  ) -> Usuario:
    usuario.is_active = False
    usuario.deactivated_at = datetime.now(timezone.utc)
    await session.flush()
    return usuario


usuario_repository = UsuarioRepository(Usuario)
