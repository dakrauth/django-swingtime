import datetime

TIMESLOT_TIME_FORMAT = '%I:%M %p'

TIMESLOT_INTERVAL = datetime.timedelta(minutes=15)

TIMESLOT_START_TIME = datetime.time(9)

TIMESLOT_END_TIME_DELTA = datetime.timedelta(hours=8)

TIMESLOT_MIN_COLUMNS = 4

# If not None, passed to the calendar module's setfirstweekday function.
CALENDAR_FIRST_WEEKDAY = 6