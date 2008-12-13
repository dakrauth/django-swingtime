import calendar
import itertools
from datetime import datetime, timedelta, time

from django import http
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from swingtime.models import Event, Occurrence
from swingtime import utils, forms
from swingtime.conf import settings as swingtime_settings

from dateutil import parser

if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


#-------------------------------------------------------------------------------
def all_events(request, template='swingtime/all_events.html', queryset=None):
    if queryset:
        queryset = queryset._clone()
    else:
        queryset = Event.objects.all()
        
    return render_to_response(
        template, 
        dict(events=queryset),
        context_instance=RequestContext(request)
    )


#-------------------------------------------------------------------------------
def view_event(
    request, 
    pk, 
    template='swingtime/event_detail.html', 
    form_class=forms.AddOccurrenceForm
):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save(event)
            return http.HttpResponseRedirect(request.path)
    else:
        form = form_class()
            
    return render_to_response(
        template, 
        dict(event=event, form=form),
        context_instance=RequestContext(request)
    )


#-------------------------------------------------------------------------------
def view_occurrence(request, event_pk, pk, template='swingtime/occurrence_detail.html'):
    return render_to_response(
        template,
        dict(occurrence=get_object_or_404(Occurrence, pk=pk, event__pk=event_pk)),
        context_instance=RequestContext(request)
    )


#-------------------------------------------------------------------------------
def add_event(request, template='swingtime/add_event.html', form_class=forms.NewEventForm):
    dtstart = None
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            event = form.save()
            return http.HttpResponseRedirect(event.get_absolute_url())
            
    else:
        if 'dtstart' in request.GET:
            try:
                dtstart = parser.parse(request.GET['dtstart'])
            except:
                # TODO A badly formatted date is passed to add_event
                pass
                
        dtstart = dtstart or datetime.now()
        dt = datetime(dtstart.year, dtstart.month, dtstart.day)
        start_time = dtstart - dt
        start_time = start_time.days * 3600 + start_time.seconds

        initial = dict(
            date=dt.date(),
            start_time=start_time,
            end_time=start_time + 3600,
            until=dtstart + timedelta(days=+7)
        )
         
        form = form_class(initial=initial)
            
    return render_to_response(
        template,
        dict(dtstart=dtstart, form=form),
        context_instance=RequestContext(request)
    )


#-------------------------------------------------------------------------------
def _datetime_view(request, dt, template):
    data = dict(
        day=dt, 
        next_day=dt + timedelta(days=+1),
        prev_day=dt + timedelta(days=-1),
        timeslots=utils.create_timeslot_table(dt)
    )
    
    return render_to_response(
        template,
        data,
        context_instance=RequestContext(request)
    )


#-------------------------------------------------------------------------------
def daily_view(request, year, month, day, template='swingtime/daily_view.html'):
    return _datetime_view(
        request, 
        datetime(int(year), int(month), int(day)), 
        template
    )


#-------------------------------------------------------------------------------
def view_today(request, template='swingtime/daily_view.html'):
    return _datetime_view(request, datetime.now(), template)


#-------------------------------------------------------------------------------
def annual_view(request, year, template='swingtime/annual_view.html'):
    pass


#-------------------------------------------------------------------------------
def monthly_view(request, year, month, template='swingtime/monthly_view.html'):
    year, month = int(year), int(month)

    cal = calendar.monthcalendar(year, month)
    dtstart = datetime(year, month, 1)
    last_day = max(cal[-1])
    dtend = datetime(year, month, last_day)

    # TODO Whether to include those occurrences that started in the previous
    # month but end in this month?
    occurrences = Occurrence.objects.select_related().filter(
        start_time__year=year,
        start_time__month=month
    )

    by_day = dict([
        (dom,list(items)) 
        for dom,items in itertools.groupby(occurrences, lambda o: o.start_time.day)
    ])
    
    data = dict(
        today=datetime.now(),
        calendar=[[(d, by_day.get(d, None)) for d in row] for row in cal], 
        this_month=dtstart,
        next_month=dtstart + timedelta(days=+last_day),
        last_month=dtstart + timedelta(days=-1),
    )

    return render_to_response(
        template, 
        data,
        context_instance=RequestContext(request)
    )


