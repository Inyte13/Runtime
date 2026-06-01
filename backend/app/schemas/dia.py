from datetime import date

from app.schemas.bloque import BloqueResponse
from app.schemas.categoria import CategoriaResumen
from pydantic import BaseModel, field_validator


class DiaResponse(BaseModel):
  model_config = {'from_attributes': True}

  fecha: date
  titulo: str | None = None


class DiaResponseDetail(DiaResponse):
  bloques: list[BloqueResponse]


class DiaResumen(DiaResponse):
  categorias: list[CategoriaResumen]


class DiaUpdate(BaseModel):
  titulo: str | None = None

  @field_validator('titulo')
  def formatear_str_vacio(cls, v: str | None) -> str | None:
    if v == '' or v is None:
      return None
    return v
