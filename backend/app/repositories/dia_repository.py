import uuid
from collections.abc import Sequence
from datetime import date

from app.models.actividad import Actividad
from app.models.actividad_oculta import ActividadOculta
from app.models.bloque import Bloque
from app.models.dia import Dia
from app.schemas.dia import DiaUpdate
from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class DiaRepository:
  async def create(self, session: AsyncSession, dia: Dia) -> Dia:
    session.add(dia)
    await session.flush()
    await session.refresh(dia)
    return dia

  async def get(
    self, session: AsyncSession, fecha: date, id_usuario: uuid.UUID
  ) -> Dia | None:
    # Solo para pk compuesta
    return await session.get(Dia, (fecha, id_usuario))

  async def get_detail(
    self, session: AsyncSession, fecha: date, id_usuario: uuid.UUID
  ) -> Dia | None:
    statement = (
      select(Dia)
      .where(Dia.fecha == fecha)
      .where(Dia.id_usuario == id_usuario)
      .options(selectinload(Dia.bloques))
    )
    result = await session.execute(statement)
    return result.scalars().first()

  async def get_resumen_by_range(
    self,
    session: AsyncSession,
    inicio: date,
    final: date,
    id_usuario: uuid.UUID,
  ) -> Sequence[Dia]:
    statement = (
      select(Dia)
      .where(Dia.id_usuario == id_usuario)
      .where(inicio <= Dia.fecha)
      .where(Dia.fecha <= final)
      .order_by(Dia.fecha)
      .options(selectinload(Dia.bloques))
    )
    result = await session.execute(statement)
    return result.scalars().all()

  async def get_bloques_resumen(
    self, session: AsyncSession, fecha: date, id_usuario: uuid.UUID
  ) -> Sequence[Row[tuple[uuid.UUID, float, str | None, uuid.UUID]]]:
    subquery = select(ActividadOculta.id_actividad).where(
      ActividadOculta.id_usuario == id_usuario
    )
    statement = (
      select(
        Bloque.id_actividad,
        Bloque.duracion,
        Bloque.descripcion,
        Actividad.id_categoria,
      )
      .join(Actividad)
      .where(Bloque.fecha == fecha)
      .where(Bloque.id_usuario == id_usuario)
      .where(Actividad.id.notin_(subquery))
    )
    result = await session.execute(statement)
    return result.all()

  async def update(
    self, session: AsyncSession, dia_obj: Dia, dia: DiaUpdate
  ) -> Dia:
    update_data = dia.model_dump(exclude_unset=True)
    # Parseamos de dict directamente actualizar los campos
    for field, value in update_data.items():
      setattr(dia_obj, field, value)
    await session.flush()
    await session.refresh(dia_obj)
    return dia_obj

  async def delete(self, session: AsyncSession, dia: Dia) -> None:
    return await session.delete(dia)


dia_repository = DiaRepository()
