from collections.abc import Sequence
from datetime import time

from app.core.exceptions.time_exception import (
  TimeBoundaryError,
)
from app.models.block import Block


def hour_end_to_minutes(hour_end: time) -> int:
  if hour_end == time(0, 0):
    return 1440
  return hour_end.hour * 60 + hour_end.minute


def minutes_to_hours(minutes: int) -> time:
  if minutes == 1440:
    return time(0, 0)
  return time(minutes // 60, minutes % 60)


def add_duration_in_minutes(hour: time, duration: float) -> int:
  return hour.hour * 60 + hour.minute + int(duration * 60)


def calculate_hour_end(hour: time, duration: float) -> time:
  new_hour_end_in_minutes = add_duration_in_minutes(hour, duration)
  if new_hour_end_in_minutes > 1440:
    raise TimeBoundaryError()
  return minutes_to_hours(new_hour_end_in_minutes)


def recalculate_hours(blocks: Sequence[Block], difference: float) -> None:
  difference_in_minutes = int(difference * 60)
  last_block = blocks[-1]

  if hour_end_to_minutes(last_block.hour_end) + difference_in_minutes > 1440:
    raise TimeBoundaryError()

  for block in blocks:
    new_hour_in_minutes = add_duration_in_minutes(
      block.hour,
      difference,
    )
    new_hour_end_in_minutes = (
      hour_end_to_minutes(block.hour_end) + difference_in_minutes
    )

    block.hour = minutes_to_hours(new_hour_in_minutes)
    block.hour_end = minutes_to_hours(new_hour_end_in_minutes)
