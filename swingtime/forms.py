'''
Convenience forms for adding and updating ``Event`` and ``Occurrence``s.
'''
from datetime import datetime, date, time, timedelta
from django import forms
from django.forms.utils import to_current_timezone
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import SelectDateWidget

from dateutil import rrule
from .conf import swingtime_settings
from .models import *
from . import utils

WEEKDAY_SHORT = (
    (7, _('Sun')),
    (1, _('Mon')),
    (2, _('Tue')),
    (3, _('Wed')),
    (4, _('Thu')),
    (5, _('Fri')),
    (6, _('Sat'))
)

WEEKDAY_LONG = (
    (7, _('Sunday')),
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday'))
)

MONTH_LONG = (
    (1,  _('January')),
    (2,  _('February')),
    (3,  _('March')),
    (4,  _('April')),
    (5,  _('May')),
    (6,  _('June')),
    (7,  _('July')),
    (8,  _('August')),
    (9,  _('September')),
    (10, _('October')),
    (11, _('November')),
    (12, _('December')),
)

MONTH_SHORT = (
    (1,  _('Jan')),
    (2,  _('Feb')),
    (3,  _('Mar')),
    (4,  _('Apr')),
    (5,  _('May')),
    (6,  _('Jun')),
    (7,  _('Jul')),
    (8,  _('Aug')),
    (9,  _('Sep')),
    (10, _('Oct')),
    (11, _('Nov')),
    (12, _('Dec')),
)


ORDINAL = (
    (1,  _('first')),
    (2,  _('second')),
    (3,  _('third')),
    (4,  _('fourth')),
    (-1, _('last'))
)

FREQUENCY_CHOICES = (
    (rrule.DAILY,   _('Day(s)')),
    (rrule.WEEKLY,  _('Week(s)')),
    (rrule.MONTHLY, _('Month(s)')),
    (rrule.YEARLY,  _('Year(s)')),
)

REPEAT_CHOICES = (
    ('count', _('By count')),
    ('until', _('Until date')),
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

MINUTES_INTERVAL = swingtime_settings.TIMESLOT_INTERVAL.seconds // 60
SECONDS_INTERVAL = utils.time_delta_total_seconds(swingtime_settings.DEFAULT_OCCURRENCE_DURATION)


def timeslot_options(
    interval=swingtime_settings.TIMESLOT_INTERVAL,
    start_time=swingtime_settings.TIMESLOT_START_TIME,
    end_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION,
    fmt=swingtime_settings.TIMESLOT_TIME_FORMAT
):
    '''
    Create a list of time slot options for use in swingtime forms.

    The list is comprised of 2-tuples containing a 24-hour time value and a
    12-hour temporal representation of that offset.

    '''
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_delta
    options = []

    while dtstart <= dtend:
        options.append((str(dtstart.time()), dtstart.strftime(fmt)))
        dtstart += interval

    return options


def timeslot_offset_options(
    interval=swingtime_settings.TIMESLOT_INTERVAL,
    start_time=swingtime_settings.TIMESLOT_START_TIME,
    end_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION,
    fmt=swingtime_settings.TIMESLOT_TIME_FORMAT
):
    '''
    Create a list of time slot options for use in swingtime forms.

    The list is comprised of 2-tuples containing the number of seconds since the
    start of the day and a 12-hour temporal representation of that offset.

    '''
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_delta
    options = []

    delta = utils.time_delta_total_seconds(dtstart - dt)
    seconds = utils.time_delta_total_seconds(interval)
    while dtstart <= dtend:
        options.append((delta, dtstart.strftime(fmt)))
        dtstart += interval
        delta += seconds

    return options


default_timeslot_options = timeslot_options()
default_timeslot_offset_options = timeslot_offset_options()


class MultipleIntegerField(forms.MultipleChoiceField):
    '''
    A form field for handling multiple integers.

    '''

    def __init__(self, choices, size=None, label=None, widget=None):
        widget = widget or forms.SelectMultiple(attrs={'size': size or len(choices)})
        super().__init__(
            required=False,
            choices=choices,
            label=label,
            widget=widget,
        )

    def clean(self, value):
        return [int(i) for i in super().clean(value)]


class SplitDateTimeWidget(forms.MultiWidget):
    '''
    A Widget that splits datetime input into a SelectDateWidget for dates and
    Select widget for times.

    '''
    def __init__(self, attrs=None):
        widgets = (
            SelectDateWidget(attrs=attrs),
            forms.Select(choices=default_timeslot_options, attrs=attrs)
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]


class MultipleOccurrenceForm(forms.Form):
    day = forms.DateField(
        label=_('Date'),
        initial=date.today,
        widget=SelectDateWidget()
    )

    start_time_delta = forms.IntegerField(
        label=_('Start time'),
        widget=forms.Select(choices=default_timeslot_offset_options)
    )

    end_time_delta = forms.IntegerField(
        label=_('End time'),
        widget=forms.Select(choices=default_timeslot_offset_options)
    )

    # recurrence options
    repeats = forms.ChoiceField(
        choices=REPEAT_CHOICES,
        initial='count',
        label=_('Occurrences'),
        widget=forms.RadioSelect()
    )

    count = forms.IntegerField(
        label=_('Total Occurrences'),
        initial=1,
        required=False,
        widget=forms.TextInput(attrs=dict(size=2, max_length=2))
    )

    until = forms.DateField(
        required=False,
        initial=date.today,
        widget=SelectDateWidget()
    )

    freq = forms.IntegerField(
        label=_('Frequency'),
        initial=rrule.WEEKLY,
        widget=forms.RadioSelect(choices=FREQUENCY_CHOICES),
    )

    interval = forms.IntegerField(
        required=False,
        initial='1',
        widget=forms.TextInput(attrs=dict(size=3, max_length=3))
    )

    # weekly options
    week_days = MultipleIntegerField(
        WEEKDAY_SHORT,
        label=_('Weekly options'),
        widget=forms.CheckboxSelectMultiple
    )

    # monthly options
    month_option = forms.ChoiceField(
        choices=(('on', _('On the')), ('each', _('Each:'))),
        initial='each',
        widget=forms.RadioSelect(),
        label=_('Monthly options')
    )

    month_ordinal = forms.IntegerField(
        widget=forms.Select(choices=ORDINAL),
        required=False
    )
    month_ordinal_day = forms.IntegerField(
        widget=forms.Select(choices=WEEKDAY_LONG),
        required=False
    )

    each_month_day = MultipleIntegerField(
        [(i, i) for i in range(1, 32)],
        widget=forms.CheckboxSelectMultiple
    )

    # yearly options
    year_months = MultipleIntegerField(
        MONTH_SHORT,
        label=_('Yearly options'),
        widget=forms.CheckboxSelectMultiple
    )

    is_year_month_ordinal = forms.BooleanField(required=False)
    year_month_ordinal = forms.IntegerField(
        widget=forms.Select(choices=ORDINAL),
        required=False
    )

    year_month_ordinal_day = forms.IntegerField(
        widget=forms.Select(choices=WEEKDAY_LONG),
        required=False
    )

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        dtstart = self.initial.get('dtstart', None)
        if dtstart:
            dtstart = dtstart.replace(
                minute=((dtstart.minute // MINUTES_INTERVAL) * MINUTES_INTERVAL),
                second=0,
                microsecond=0
            )

            weekday = dtstart.isoweekday()
            ordinal = dtstart.day // 7
            ordinal = '%d' % (-1 if ordinal > 3 else ordinal + 1,)
            midnight = datetime.combine(dtstart.date(), time(0, tzinfo=dtstart.tzinfo))
            offset = (dtstart - midnight).seconds

            self.initial.setdefault('day', dtstart)
            self.initial.setdefault('week_days', '%d' % weekday)
            self.initial.setdefault('month_ordinal', ordinal)
            self.initial.setdefault('month_ordinal_day', '%d' % weekday)
            self.initial.setdefault('each_month_day', ['%d' % dtstart.day])
            self.initial.setdefault('year_months', ['%d' % dtstart.month])
            self.initial.setdefault('year_month_ordinal', ordinal)
            self.initial.setdefault('year_month_ordinal_day', '%d' % weekday)
            self.initial.setdefault('start_time_delta', '%d' % offset)
            self.initial.setdefault('end_time_delta', '%d' % (offset + SECONDS_INTERVAL,))

    def clean(self):
        if 'day' in self.cleaned_data:
            day = datetime.combine(self.cleaned_data['day'], time(0))
            self.cleaned_data['start_time'] = day + timedelta(
                seconds=self.cleaned_data['start_time_delta']
            )

            self.cleaned_data['end_time'] = day + timedelta(
                seconds=self.cleaned_data['end_time_delta']
            )

        return self.cleaned_data

    def save(self, event):
        if self.cleaned_data['repeats'] == 'count' and self.cleaned_data['count'] == 1:
            params = {}
        else:
            params = self._build_rrule_params()

        event.add_occurrences(
            self.cleaned_data['start_time'],
            self.cleaned_data['end_time'],
            **params
        )

        return event

    def _build_rrule_params(self):
        iso = ISO_WEEKDAYS_MAP
        data = self.cleaned_data
        params = dict(
            freq=data['freq'],
            interval=data['interval'] or 1
        )

        if data['repeats'] == 'until':
            params['until'] = data['until']
        else:
            params['count'] = data.get('count', 1)

        if params['freq'] == rrule.WEEKLY:
            params['byweekday'] = [iso[n] for n in data['week_days']]

        elif params['freq'] == rrule.MONTHLY:
            if 'on' == data['month_option']:
                ordinal = data['month_ordinal']
                day = iso[data['month_ordinal_day']]
                params.update(byweekday=day, bysetpos=ordinal)
            else:
                params['bymonthday'] = data['each_month_day']

        elif params['freq'] == rrule.YEARLY:
            params['bymonth'] = data['year_months']
            if data['is_year_month_ordinal']:
                ordinal = data['year_month_ordinal']
                day = iso[data['year_month_ordinal_day']]
                params['byweekday'] = day(ordinal)

        elif params['freq'] != rrule.DAILY:
            raise NotImplementedError(_('Unknown interval rule ' + params['freq']))

        return params


class EventForm(forms.ModelForm):
    '''
    A simple form for adding and updating Event attributes

    '''

    class Meta:
        model = Event
        fields = "__all__"

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.fields['description'].required = False


class SingleOccurrenceForm(forms.ModelForm):
    '''
    A simple form for adding and updating single Occurrence attributes

    '''

    start_time = forms.SplitDateTimeField(widget=SplitDateTimeWidget)
    end_time = forms.SplitDateTimeField(widget=SplitDateTimeWidget)

    class Meta:
        model = Occurrence
        fields = "__all__"
