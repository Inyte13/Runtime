from pydantic_extra_types import Color


def color_normalize(value: Color | str) -> Color:
  if not isinstance(value, Color):
    value = Color(value)

  if len(value.as_hex(format='long')) != 7:
    raise ValueError('El color no puede tener transparencia')

  return value


def color_to_hex(value: Color | str) -> str:
  return color_normalize(value).as_hex(format='long')
