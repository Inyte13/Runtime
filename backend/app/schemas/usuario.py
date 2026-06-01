import uuid

from pydantic import BaseModel, field_validator


class UsuarioLoginGoogle(BaseModel):
  credential: str


class UsuarioResponse(BaseModel):
  model_config = {'from_attributes': True}

  id: uuid.UUID
  email: str
  given_name: str | None = None
  family_name: str | None = None
  picture_url: str | None = None
  id_actividad_default: uuid.UUID


class UsuarioUpdate(BaseModel):
  id_actividad_default: uuid.UUID | None = None

  @field_validator('id_actividad_default')
  def validar_id_actividad_default(
    cls, v: uuid.UUID | None
  ) -> uuid.UUID | None:
    if v is None:
      raise ValueError('id_actividad_default no puede ser null')
    return v
