import uuid

from pydantic import BaseModel


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
  id_actividad_default: uuid.UUID
