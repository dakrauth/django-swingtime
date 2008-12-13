from collections import defaultdict
from datetime import datetime, date, time, timedelta
import itertools

from django.utils.safestring import mark_safe

from dateutil import rrule

from swingtime.models import EventType, Occurrence
from swingtime.conf import settings as swingtime_settings

WEEKDAY_SHORT = (
    (7, 'Sun'),
    (1, 'Mon'),
    (2, 'Tue'),
    (3, 'Wed'),
    (4, 'Thu'),
    (5, 'Fri'),
    (6, 'Sat')
)

WEEKDAY_LONG = (
    (7, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday')
)

MONTH_LONG = (
    (1,  'January'),
    (2,  'February'),
    (3,  'March'),
    (4,  'April'),
    (5,  'May'),
    (6,  'June'),
    (7,  'July'),
    (8,  'August'),
    (9,  'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)


ORDINAL = (
    (1,  'first'),
    (2,  'second'),
    (3,  'third'),
    (4,  'fourth'),
    (-1, 'last')
)

ISO_WEEKDAYS_MAP = (
    None,
    rrule.MO,
    rrule.TU,
    rrule.WE,
    rrule.TH,
    rrule.FR,
    rrule.SA,
    rrule.SU
)


#-------------------------------------------------------------------------------
def html_mark_safe(func):
    def decorator(*args, **kws):
        return mark_safe(func(*args, **kws))
    return decorator


#-------------------------------------------------------------------------------
def total_seconds(time_delta):
    return time_delta.days * 3600 + time_delta.seconds
    
#-------------------------------------------------------------------------------
def time_slot_options(
    interval=swingtime_settings.TIMESLOT_INTERVAL,
    start_time=swingtime_settings.TIMESLOT_START_TIME,
    end_delta=swingtime_settings.TIMESLOT_END_TIME_DELTA,
    fmt=swingtime_settings.TIMESLOT_TIME_FORMAT
):
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_delta
    slots = []

    delta = total_seconds(dtstart - dt)
    seconds = total_seconds(interval)
    while dtstart <= dtend:
        slots.append((delta, dtstart.strftime(fmt)))
        dtstart += interval
        delta += seconds
    
    return slots    


default_time_slot_options = time_slot_options()


#-------------------------------------------------------------------------------
def month_boundaries(dt=None):
    import calendar
    dt = dt or date.today()
    wkday, ndays = calendar.monthrange(dt.year, dt.month)
    start = datetime(dt.year, dt.month, 1)
    return (start, start + timedelta(ndays - 1))


#-------------------------------------------------------------------------------
def css_class_cycler():
    return defaultdict(
        lambda: itertools.cycle(('evt-even', 'evt-odd')).next,
        ((e.abbr, itertools.cycle((
             'evt-%s-even' % e.abbr, 
             'evt-%s-odd' % e.abbr
             )).next) for e in EventType.objects.all()
        )
    )


#===============================================================================
class TimeslotRow(object):

    #---------------------------------------------------------------------------
    def __init__(self, tm, cols):
        self.time = tm
        self.columns = cols

    #---------------------------------------------------------------------------
    def __iter__(self):
        return iter(self.columns)

    #---------------------------------------------------------------------------
    def __repr__(self):
        return '<TimeslotTable.Row %s>' % self.time


#===============================================================================
class OccurrenceProxy(object):

    #---------------------------------------------------------------------------
    def __init__(self, occurrence, col):
        self.col = col
        self.occurrence = occurrence
        self.event_type = occurrence.event_type
        self.event_class = ''

        link = '<a href="%s">%s</a>' % (
            self.occurrence.get_absolute_url(),
            self.occurrence.title
        )
        
        self._str = itertools.chain((link,),itertools.repeat('///')).next

    #---------------------------------------------------------------------------
    @html_mark_safe
    def __unicode__(self):
        return self._str()


#-------------------------------------------------------------------------------
def create_timeslot_table(
    dt=None,
    items=None,
    start_time=swingtime_settings.TIMESLOT_START_TIME,
    end_time_delta=swingtime_settings.TIMESLOT_END_TIME_DELTA,
    time_delta=swingtime_settings.TIMESLOT_INTERVAL,
    min_columns=swingtime_settings.TIMESLOT_MIN_COLUMNS,
    css_class_cycles=css_class_cycler,
    proxy_class=OccurrenceProxy
):
    dt = dt or datetime.now()
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_time_delta
    items = items or Occurrence.objects.daily_occurrences(dt).select_related('event')
    timeslots = dict()
    n = dtstart
    while n <= dtend:
        timeslots[n] = {}
        n += time_delta

    for item in sorted(items):
        if item.end_time <= dtstart:
            continue

        if item.start_time > dtstart:
            rowkey = current = item.start_time
        else:
            rowkey = current = dtstart

        timeslot = timeslots.get(rowkey, None)
        if timeslot is None:
            continue

        colkey = 0
        while 1:
            if colkey not in timeslot:
                proxy = proxy_class(item, colkey)
                timeslot[colkey] = proxy

                while current < item.end_time:
                    rowkey = current
                    row = timeslots.get(rowkey, None)
                    if row is None:
                        break

                    row[colkey] = proxy
                    current += time_delta
                break

            colkey += 1

    # determine the number of timeslot columns we should show
    column_lens = [len(x) for x in timeslots.itervalues()]
    max_column_len = max(column_lens) if column_lens else 0
    ncol = max((min_columns, max_column_len))
    colclasses = dict([(i, css_class_cycles()) for i in range(ncol)])
    empty_cols = ['' for x in range(ncol)]

    from pprint import pprint
    # pprint(timeslots)
    table = []
    for rowkey in sorted(timeslots.keys()):
        cols = empty_cols[:]
        for colkey in timeslots[rowkey]:
            proxy = timeslots[rowkey][colkey]
            cols[colkey] = proxy
            if not proxy.event_class:
                proxy.event_class = colclasses[colkey][proxy.event_type.abbr]()
                # print colkey, proxy.event_class

        table.append(TimeslotRow(rowkey, cols))

    return table
