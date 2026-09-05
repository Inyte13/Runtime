import uuid

from pydantic import BaseModel


class UserLoginGoogle(BaseModel):
  credential: str


class UserResponse(BaseModel):
  model_config = {'from_attributes': True}

  id: uuid.UUID
  email: str
  given_name: str | None = None
  family_name: str | None = None
  picture_url: str | None = None
  default_activity_id: uuid.UUID


class UserUpdate(BaseModel):
  default_activity_id: uuid.UUID
