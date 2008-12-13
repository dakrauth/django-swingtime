from datetime import datetime, date, time, timedelta
from cStringIO import StringIO

from django import forms
from django import http
from django import forms
from django.forms.util import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import DEFAULT_DATETIME_INPUT_FORMATS, EMPTY_VALUES

from dateutil import rrule
from swingtime import utils
from swingtime.conf import settings as swingtime_settings
from swingtime.models import *


EXTENDED_DATETIME_INPUT_FORMATS = DEFAULT_DATETIME_INPUT_FORMATS + (
    '%Y%m%dT%H%M%S',
    '%Y%m%dT%H%M',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M',
)

EVENT_TITLE_LENGTH = Event._meta.get_field('title').max_length

num_attrs = { 'onkeypress' : "return OnlyNumbers(event);" }

frequency_choices = (
    (rrule.DAILY,   'Day(s)'),
    (rrule.WEEKLY,  'Week(s)'),
    (rrule.MONTHLY, 'Month(s)'),
    (rrule.YEARLY,  'Year(s)'),
)

repeat_choices = (
    ('count', 'By count'),
    ('until', 'Until date'),
)

#===============================================================================
class MultipleIntegerField(forms.MultipleChoiceField):

    #---------------------------------------------------------------------------
    def __init__(self, choices, size=None, label=None):
        size = size or len(choices)
        super(MultipleIntegerField, self).__init__(
            required=False,
            choices=choices,
            label=label,
            widget=forms.SelectMultiple(attrs={'size' : size}),
        )

    #---------------------------------------------------------------------------
    def clean(self, value):
        return [int(i) for i in super(MultipleIntegerField, self).clean(value)]


#===============================================================================
class AddOccurrenceForm(forms.Form):
    day = forms.DateField(
        label='Date',
        initial=date.today,
        widget=SelectDateWidget()
    )
    
    start_time_delta = forms.IntegerField(
        label='Start time',
        widget=forms.Select(choices=utils.default_time_slot_options)
    )
    
    end_time_delta = forms.IntegerField(
        label='End time',
        widget=forms.Select(choices=utils.default_time_slot_options)
    )

    # recurrence options
    repeats = forms.ChoiceField(
        choices=repeat_choices,
        initial='count',
        label='Occurrences',
        widget=forms.RadioSelect()
    )

    count = forms.IntegerField(
        label='Total Occurrences',
        initial=1,
        required=False,
        widget=forms.TextInput(attrs=dict(num_attrs, size=2, max_length=2))
    )

    until = forms.DateField(
        required=False,
        initial=date.today,
        widget=SelectDateWidget()
    )
    
    freq = forms.IntegerField(
        label='Frequency',
        initial=rrule.WEEKLY,
        widget=forms.Select(choices=frequency_choices)
    )

    interval = forms.IntegerField(
        required=False,
        initial='1',
        widget=forms.TextInput(attrs=dict(num_attrs, size=3, max_length=3))
    )
    
    # weekly options
    week_days = MultipleIntegerField(utils.WEEKDAY_LONG, label='Weekly options')
    
    # monthly  options
    month_option = forms.ChoiceField(
        choices=(('on','On the'), ('each','Each:')),
        initial='each',
        widget=forms.RadioSelect(),
        label='Monthly options'
    )
    
    month_ordinal = forms.IntegerField(widget=forms.Select(choices=utils.ORDINAL))
    month_ordinal_day = forms.IntegerField(widget=forms.Select(choices=utils.WEEKDAY_LONG))
    each_month_day = MultipleIntegerField([(i,i) for i in range(1,32)], 10)
    
    # yearly options
    year_months = MultipleIntegerField(utils.MONTH_LONG, label='Yearly options')
    is_year_month_ordinal = forms.BooleanField(required=False)
    year_month_ordinal = forms.IntegerField(widget=forms.Select(choices=utils.ORDINAL))
    year_month_ordinal_day = forms.IntegerField(widget=forms.Select(choices=utils.WEEKDAY_LONG))
    
    #---------------------------------------------------------------------------
    def __init__(self, *args, **kws):
        super(AddOccurrenceForm, self).__init__(*args, **kws)
    
    #---------------------------------------------------------------------------
    def clean(self):
        day = datetime.combine(self.cleaned_data['day'], time(0))
        self.cleaned_data['start_time'] = day + timedelta(
            seconds=self.cleaned_data['start_time_delta']
        )
        
        self.cleaned_data['end_time'] = day + timedelta(
            seconds=self.cleaned_data['end_time_delta']
        )
        
        return self.cleaned_data

    #---------------------------------------------------------------------------
    def save(self, event):
        if self.cleaned_data['repeats'] == 'no':
            params = {}
        else:
            params = self._build_rrule_params()

        event.add_occurrences(
            self.cleaned_data['start_time'], 
            self.cleaned_data['end_time'],
            **params
        )

        return event

    #---------------------------------------------------------------------------
    def _build_rrule_params(self):
        iso = utils.ISO_WEEKDAYS_MAP
        data = self.cleaned_data
        params = dict(
            freq=data['freq'],
            #dtstart=data['start_time'],
            interval=data['interval'] or 1
        )
        
        if self.cleaned_data['repeats'] == 'count':
            params['count'] = data['count']
        elif self.cleaned_data['repeats'] == 'until':
            params['until'] = data['until']

        if params['freq'] == rrule.WEEKLY:
            params['byweekday'] = [iso[n] for n in data['week_days']]

        elif params['freq'] == rrule.MONTHLY:
            if 'on' == data['month_option']:
                ordinal = data['month_ordinal']
                day = iso[data['month_ordinal_day']]
                params['byweekday'] = day(ordinal)
            else:
                params['bymonthday'] = data['each_month_day']

        elif params['freq'] == rrule.YEARLY:
            params['bymonth'] = data['year_months']
            if data['is_year_month_ordinal']:
                ordinal = data['year_month_ordinal']
                day = iso[data['year_month_ordinal_day']]
                params['byweekday'] = day(ordinal)
                
        elif params['freq'] != rrule.DAILY:
            raise NotImplementedError('Unknown interval rule %s' % params['freq'])

        return params


#===============================================================================
class NewEventForm(AddOccurrenceForm):
    event_type = forms.ModelChoiceField(EventType.objects)
    
    title = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs=dict(size=32))
    )
    
    description = forms.CharField(
        label='Description', 
        required=False, 
        max_length=100,
        widget=forms.TextInput(attrs=dict(size=50)),
    )

    #---------------------------------------------------------------------------
    def save(self):
        event = Event.objects.create(
            title=self.cleaned_data['title'], 
            event_type=self.cleaned_data['event_type'],
            description=self.cleaned_data['description']
        )
        
        super(NewEventForm, self).save(self)
        return event

        
