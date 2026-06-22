class InvalidTimeGranularityError(Exception):
  pass


class TimeBoundaryError(Exception):
  def __init__(self, detail: str = 'El bloque se pasa de medianoche'):
    super().__init__(detail)
