from app.domain.colors import color_normalize, color_to_hex
from pydantic_extra_types import Color
from sqlalchemy import Dialect, String, TypeDecorator


class ColorType(TypeDecorator[Color]):
  # El tipo real en la bd
  impl = String(7)
  cache_ok = True

  # py -> bd
  def process_bind_param(
    self, value: Color | None, dialect: Dialect
  ) -> str | None:
    if value is None:
      return None
    return color_to_hex(value)

  # bd -> py
  def process_result_value(
    self, value: str | None, dialect: Dialect
  ) -> Color | None:
    if value is None:
      return None
    return color_normalize(value)
