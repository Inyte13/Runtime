from datetime import time

from app.core.exceptions.time import (
  InvalidTimeGranularityError,
  TimeBoundaryError,
)


def modificar_hora(hora: time, duracion: float) -> time:
  # Calculamos pero en minutos, por las 24:00
  minutos_inicio = hora.hour * 60 + hora.minute
  minutos_fin = minutos_inicio + int(duracion * 60)
  if minutos_fin == 1440:
    return time(0, 0)
  if minutos_fin > 1440:
    raise TimeBoundaryError()
  return time(minutos_fin // 60, minutos_fin % 60)


def validar_hora_granulidad(hora: time, unidad_duracion: int = 30) -> None:
  if (
    hora.minute % unidad_duracion != 0
    or hora.second != 0
    or hora.microsecond != 0
  ):
    raise InvalidTimeGranularityError(
      f'La hora debe estar en múltiplos de {unidad_duracion} minutos'
    )
