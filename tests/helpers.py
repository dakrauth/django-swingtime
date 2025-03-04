from datetime import datetime
from django.utils import timezone


def dt_get(yr, mo, day=1, hr=0, mn=0, sec=0, tzinfo=True):
    if tzinfo:
        tzinfo = timezone.get_default_timezone() if tzinfo is True else tzinfo

    if tzinfo is False:
        tzinfo = None

    return datetime(yr, mo, day, hr, mn, sec, tzinfo=tzinfo)


def dt_combine(day, tm, tzinfo=True):
    dt = datetime.combine(day, tm)
    return dt_get(*dt.timetuple()[:6], tzinfo=tzinfo)
