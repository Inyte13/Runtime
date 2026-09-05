import uuid

from pydantic import BaseModel


class HiddenActivityCreate(BaseModel):
  activity_id: uuid.UUID


class HiddenActivityResponse(BaseModel):
  # Si no lo armo yo, va
  model_config = {'from_attributes': True}
  activity_id: uuid.UUID
