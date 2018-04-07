import calendar
import itertools
import logging
from datetime import datetime, timedelta, time
from dateutil import parser
from django import http
from django.db import models
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render

from .models import Event, Occurrence
from . import utils, forms
from .conf import swingtime_settings


if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


def event_listing(
    request,
    template='swingtime/event_list.html',
    events=None,
    **extra_context
):
    '''
    View all ``events``.

    If ``events`` is a queryset, clone it. If ``None`` default to all ``Event``s.

    Context parameters:

    ``events``
        an iterable of ``Event`` objects

    ... plus all values passed in via **extra_context
    '''
    events = events or Event.objects.all()
    extra_context['events'] = events
    return render(request, template, extra_context)


def event_view(
    request,
    pk,
    template='swingtime/event_detail.html',
    event_form_class=forms.EventForm,
    recurrence_form_class=forms.MultipleOccurrenceForm
):
    '''
    View an ``Event`` instance and optionally update either the event or its
    occurrences.

    Context parameters:

    ``event``
        the event keyed by ``pk``

    ``event_form``
        a form object for updating the event

    ``recurrence_form``
        a form object for adding occurrences
    '''
    event = get_object_or_404(Event, pk=pk)
    event_form = recurrence_form = None
    if request.method == 'POST':
        if '_update' in request.POST:
            event_form = event_form_class(request.POST, instance=event)
            if event_form.is_valid():
                event_form.save(event)
                return http.HttpResponseRedirect(request.path)
        elif '_add' in request.POST:
            recurrence_form = recurrence_form_class(request.POST)
            if recurrence_form.is_valid():
                recurrence_form.save(event)
                return http.HttpResponseRedirect(request.path)
        else:
            return http.HttpResponseBadRequest('Bad Request')

    data = {
        'event': event,
        'event_form': event_form or event_form_class(instance=event),
        'recurrence_form': recurrence_form or recurrence_form_class(
            initial={'dtstart': datetime.now()}
        )
    }
    return render(request, template, data)


def occurrence_view(
    request,
    event_pk,
    pk,
    template='swingtime/occurrence_detail.html',
    form_class=forms.SingleOccurrenceForm
):
    '''
    View a specific occurrence and optionally handle any updates.

    Context parameters:

    ``occurrence``
        the occurrence object keyed by ``pk``

    ``form``
        a form object for updating the occurrence
    '''
    occurrence = get_object_or_404(Occurrence, pk=pk, event__pk=event_pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=occurrence)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(request.path)
    else:
        form = form_class(instance=occurrence)

    return render(request, template, {'occurrence': occurrence, 'form': form})


def add_event(
    request,
    template='swingtime/add_event.html',
    event_form_class=forms.EventForm,
    recurrence_form_class=forms.MultipleOccurrenceForm
):
    '''
    Add a new ``Event`` instance and 1 or more associated ``Occurrence``s.

    Context parameters:

    ``dtstart``
        a datetime.datetime object representing the GET request value if present,
        otherwise None

    ``event_form``
        a form object for updating the event

    ``recurrence_form``
        a form object for adding occurrences

    '''
    dtstart = None
    if request.method == 'POST':
        event_form = event_form_class(request.POST)
        recurrence_form = recurrence_form_class(request.POST)
        if event_form.is_valid() and recurrence_form.is_valid():
            event = event_form.save()
            recurrence_form.save(event)
            return http.HttpResponseRedirect(event.get_absolute_url())

    else:
        if 'dtstart' in request.GET:
            try:
                dtstart = parser.parse(request.GET['dtstart'])
            except(TypeError, ValueError) as exc:
                # TODO: A badly formatted date is passed to add_event
                logging.warning(exc)

        dtstart = dtstart or datetime.now()
        event_form = event_form_class()
        recurrence_form = recurrence_form_class(initial={'dtstart': dtstart})

    return render(
        request,
        template,
        {'dtstart': dtstart, 'event_form': event_form, 'recurrence_form': recurrence_form}
    )


def _datetime_view(
    request,
    template,
    dt,
    timeslot_factory=None,
    items=None,
    params=None
):
    '''
    Build a time slot grid representation for the given datetime ``dt``. See
    utils.create_timeslot_table documentation for items and params.

    Context parameters:

    ``day``
        the specified datetime value (dt)

    ``next_day``
        day + 1 day

    ``prev_day``
        day - 1 day

    ``timeslots``
        time slot grid of (time, cells) rows

    '''
    timeslot_factory = timeslot_factory or utils.create_timeslot_table
    params = params or {}

    return render(request, template, {
        'day':       dt,
        'next_day':  dt + timedelta(days=+1),
        'prev_day':  dt + timedelta(days=-1),
        'timeslots': timeslot_factory(dt, items, **params)
    })


def day_view(request, year, month, day, template='swingtime/daily_view.html', **params):
    '''
    See documentation for function``_datetime_view``.

    '''
    dt = datetime(int(year), int(month), int(day))
    return _datetime_view(request, template, dt, **params)


def today_view(request, template='swingtime/daily_view.html', **params):
    '''
    See documentation for function``_datetime_view``.

    '''
    return _datetime_view(request, template, datetime.now(), **params)


def year_view(request, year, template='swingtime/yearly_view.html', queryset=None):
    '''

    Context parameters:

    ``year``
        an integer value for the year in questin

    ``next_year``
        year + 1

    ``last_year``
        year - 1

    ``by_month``
        a sorted list of (month, occurrences) tuples where month is a
        datetime.datetime object for the first day of a month and occurrences
        is a (potentially empty) list of values for that month. Only months
        which have at least 1 occurrence is represented in the list

    '''
    year = int(year)
    queryset = queryset._clone() if queryset is not None else Occurrence.objects.select_related()
    occurrences = queryset.filter(
        models.Q(start_time__year=year) |
        models.Q(end_time__year=year)
    )

    def group_key(o):
        return datetime(
            year,
            o.start_time.month if o.start_time.year == year else o.end_time.month,
            1
        )

    return render(request, template, {
        'year': year,
        'by_month': [(dt, list(o)) for dt, o in itertools.groupby(occurrences, group_key)],
        'next_year': year + 1,
        'last_year': year - 1

    })


def month_view(
    request,
    year,
    month,
    template='swingtime/monthly_view.html',
    queryset=None
):
    '''
    Render a tradional calendar grid view with temporal navigation variables.

    Context parameters:

    ``today``
        the current datetime.datetime value

    ``calendar``
        a list of rows containing (day, items) cells, where day is the day of
        the month integer and items is a (potentially empty) list of occurrence
        for the day

    ``this_month``
        a datetime.datetime representing the first day of the month

    ``next_month``
        this_month + 1 month

    ``last_month``
        this_month - 1 month

    '''
    year, month = int(year), int(month)
    cal = calendar.monthcalendar(year, month)
    dtstart = datetime(year, month, 1)
    last_day = max(cal[-1])
    dtend = datetime(year, month, last_day)

    # TODO Whether to include those occurrences that started in the previous
    # month but end in this month?
    queryset = queryset._clone() if queryset is not None else Occurrence.objects.select_related()
    occurrences = queryset.filter(start_time__year=year, start_time__month=month)

    def start_day(o):
        return o.start_time.day

    by_day = dict([(dt, list(o)) for dt, o in itertools.groupby(occurrences, start_day)])
    data = {
        'today':      datetime.now(),
        'calendar':   [[(d, by_day.get(d, [])) for d in row] for row in cal],
        'this_month': dtstart,
        'next_month': dtstart + timedelta(days=+last_day),
        'last_month': dtstart + timedelta(days=-1),
    }

    return render(request, template, data)
