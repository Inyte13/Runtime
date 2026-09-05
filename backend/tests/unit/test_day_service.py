import uuid
from datetime import date
from uuid import uuid4

from app.core.constants import GRANULARITY_HOURS
from app.services.day_service import day_service


def test_build_day_calendar():
  test_date = date(2026, 5, 20)
  category_a_id = uuid4()
  activity_a1_id = uuid4()
  activity_a2_id = uuid4()

  category_b_id = uuid4()
  activity_b1_id = uuid4()
  activity_b2_id = uuid4()

  category_c_id = uuid4()
  activity_c1_id = uuid4()
  activity_c2_id = uuid4()
  tuples: list[tuple[date, uuid.UUID, float, str | None, uuid.UUID]] = [
    (
      test_date,
      activity_a1_id,
      GRANULARITY_HOURS,
      'Description 0',
      category_a_id,
    ),
    (test_date, activity_a2_id, GRANULARITY_HOURS, None, category_a_id),
    (
      test_date,
      activity_b2_id,
      GRANULARITY_HOURS * 2,
      'Description 1',
      category_b_id,
    ),
    (
      test_date,
      activity_b1_id,
      GRANULARITY_HOURS,
      'Description 2',
      category_b_id,
    ),
    (test_date, activity_b1_id, GRANULARITY_HOURS, None, category_b_id),
    (
      test_date,
      activity_c1_id,
      GRANULARITY_HOURS * 4,
      'Description 4',
      category_c_id,
    ),
    (
      test_date,
      activity_c2_id,
      GRANULARITY_HOURS,
      'Description 3',
      category_c_id,
    ),
  ]
  days_calendar = day_service.build_day_calendar(tuples, test_date)

  # category_c: 5n
  # activity_c1_id: 4n
  # activity_c2_id: 1n

  # category_b: 4n
  # activity_b2_id: 2n
  # activity_b1_id: 1n
  # activity_b1_id: 1n

  # category_a: 2h
  # activity_a2_id: 1n
  # activity_a1_id: 1n

  category_c = days_calendar.categories[0]
  activity_c1 = category_c.activities[0]
  activity_c2 = category_c.activities[1]

  category_b = days_calendar.categories[1]
  activity_b2 = category_b.activities[0]

  activity_b1 = None
  for activity in category_b.activities:
    if activity.id == activity_b1_id:
      activity_b1 = activity
      break

  category_a = days_calendar.categories[2]

  assert days_calendar.date == test_date
  assert days_calendar.title is None
  assert days_calendar.duration == 5.5

  assert category_c.id == category_c_id
  assert category_c.duration == GRANULARITY_HOURS * 5

  assert activity_c1.id == activity_c1_id
  assert activity_c1.duration == GRANULARITY_HOURS * 4
  assert activity_c1.descriptions == ['Description 4']

  assert activity_c2.id == activity_c2_id
  assert activity_c2.duration == GRANULARITY_HOURS
  assert activity_c2.descriptions == ['Description 3']

  assert category_b.id == category_b_id
  assert category_b.duration == GRANULARITY_HOURS * 4
  assert len(category_b.activities) == 2
  assert activity_b1 is not None
  assert activity_b1.duration == GRANULARITY_HOURS * 2
  assert activity_b1.descriptions == ['Description 2']

  assert activity_b2.id == activity_b2_id
  assert activity_b2.duration == GRANULARITY_HOURS * 2
  assert activity_b2.descriptions == ['Description 1']

  assert category_a.id == category_a_id
  assert category_a.duration == GRANULARITY_HOURS * 2
  assert len(category_a.activities) == 2
