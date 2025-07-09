import datetime

from django.conf import settings
from django.urls import reverse as _reverse

DEFAULT_SETTINGS = {
    # A "strftime" string for formatting start and end time selectors in forms
    "TIMESLOT_TIME_FORMAT": "%I:%M %p",
    # Used for creating start and end time form selectors as well as time slot grids.
    # Value should be datetime.timedelta value representing the incremental
    # differences between temporal options
    "TIMESLOT_INTERVAL": datetime.timedelta(minutes=15),
    # A datetime.time value indicting the starting time for time slot grids and form selectors
    "TIMESLOT_START_TIME": datetime.time(9),
    # A datetime.timedelta value indicating the offset value from
    # TIMESLOT_START_TIME for creating time slot grids and form selectors. The for
    # using a time delta is that it possible to span dates. For instance, one could
    # have a starting time of 3pm (15:00) and wish to indicate a ending value
    # 1:30am (01:30), in which case a value of datetime.timedelta(hours=10.5)
    # could be specified to indicate that the 1:30 represents the following date's
    # time and not the current date.
    "TIMESLOT_END_TIME_DURATION": datetime.timedelta(hours=+8),
    # Indicates a minimum value for the number grid columns to be shown in the time slot table.
    "TIMESLOT_MIN_COLUMNS": 4,
    # Indicate the default length in time for a new occurrence, specifed by using
    # a datetime.timedelta object
    "DEFAULT_OCCURRENCE_DURATION": datetime.timedelta(hours=+1),
    # If not None, passed to the calendar module's setfirstweekday function.
    "CALENDAR_FIRST_WEEKDAY": 6,
    "HTML_CONTINUATION_STRING": "^^^",
    "EVENT_LIST_VIEW_MODEL": "swingtime.models.Event",
    "DAY_VIEW_OCCURRENCE_CLS": "swingtime.models.Occurrence",
    "MONTH_VIEW_MODEL": "swingtime.models.Occurrence",
    "YEAR_VIEW_MODEL": "swingtime.models.Occurrence",
    "DAY_VIEW_EVENT_TYPE_CLS": "swingtime.models.EventType",
    "CREATE_EVENT_VIEW_MODEL": "swingtime.models.Event",
    "CREATE_EVENT_VIEW_FORM": "swingtime.forms.EventOccurrenceForm",
    "EVENT_VIEW_MODEL": "swingtime.models.Event",
    "EVENT_VIEW_FORM": "swingtime.forms.EventOccurrenceForm",
    "OCCURRENCE_VIEW_MODEL": "swingtime.models.Occurrence",
    "OCCURRENCE_VIEW_FORM": "swingtime.forms.SingleOccurrenceForm",
}


class swingtime_settings:
    def __getattr__(self, attr):
        if attr in getattr(settings, "SWINGTIME", {}):
            return settings.SWINGTIME[attr]

        if attr not in DEFAULT_SETTINGS:
            raise AttributeError(f"Unknown swingtime config attribute {attr}")

        return DEFAULT_SETTINGS[attr]

    def reverse(self, stem, *args, **kwargs):
        return _reverse(f"swingtime:{stem}", *args, **kwargs)


swingtime_settings = swingtime_settings()
