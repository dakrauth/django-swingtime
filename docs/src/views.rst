================================
:mod:`views` --- Swingtime Views
================================

.. module:: views

Functions
=========

``event_listing``
-----------------

.. function:: event_listing(request [, template='swingtime/event_list.html', events=None, **extra_context])

    View all ``events``. 
    
    If ``events`` is a queryset, clone it. If ``None`` default to all ``Event`` objects.
    
    Context parameters:
    
    events
        an iterable of ``Event`` objects
        
    extra_context
        extra variables passed to the template context


``event_view``
--------------

.. function:: event_view(request, pk [, template='swingtime/event_detail.html', event_form_class=forms.EventForm, recurrence_form_class=forms.MultipleOccurrenceForm])

    View an ``Event`` instance and optionally update either the event or its
    occurrences.

    Context parameters:

    event
        the event keyed by ``pk``
        
    event_form
        a form object for updating the event
        
    recurrence_form
        a form object for adding occurrences


``occurrence_view``
-------------------

.. function:: occurrence_view(request, event_pk, pk [, template='swingtime/occurrence_detail.html', form_class=forms.SingleOccurrenceForm])

    View a specific occurrence and optionally handle any updates.
    
    Context parameters:
    
    occurrence
        the occurrence object keyed by ``pk``

    form
        a form object for updating the occurrence


``add_event``
-------------

.. function:: add_event(request [,template='swingtime/add_event.html', event_form_class=forms.EventForm, recurrence_form_class=forms.MultipleOccurrenceForm])

    Add a new ``Event`` instance and 1 or more associated ``Occurrence`` instancess.
    
    Context parameters:
    
    dtstart
        a datetime.datetime object representing the GET request value if present,
        otherwise None
    
    event_form
        a form object for updating the event

    recurrence_form
        a form object for adding occurrences
    

``_datetime_view``
------------------

.. function:: _datetime_view(request template, dt, [timeslot_factory=None, items=None,params=None])

    Build a time slot grid representation for the given datetime ``dt``. See
    utils.create_timeslot_table documentation for items and params.
    
    Context parameters:
    
    day
        the specified datetime value (dt)
        
    next_day
        day + 1 day
        
    prev_day
        day - 1 day
        
    timeslots
        time slot grid of (time, cells) rows
        

``day_view``
------------

.. function:: day_view(request, year, month, day [, template='swingtime/daily_view.html', **params])

    See documentation for function``_datetime_view``.
    

``today_view``
--------------

.. function:: today_view(request [, template='swingtime/daily_view.html', **params])

    See documentation for function``_datetime_view``.
    

``year_view``
-------------

.. function:: year_view(request, year [, template='swingtime/yearly_view.html', queryset=None])

    Context parameters:
    
    year
        an integer value for the year in questin
        
    next_year
        year + 1
        
    last_year
        year - 1
        
    by_month
        a sorted list of (month, occurrences) tuples where month is a 
        datetime.datetime object for the first day of a month and occurrences
        is a (potentially empty) list of values for that month. Only months 
        which have at least 1 occurrence is represented in the list
        

``month_view``
--------------

.. function:: month_view(request, year, month, [template='swingtime/monthly_view.html', queryset=None])

    Render a tradional calendar grid view with temporal navigation variables.

    Context parameters:
    
    today
        the current datetime.datetime value
        
    calendar
        a list of rows containing (day, items) cells, where day is the day of
        the month integer and items is a (potentially empty) list of occurrence
        for the day
        
    this_month
        a datetime.datetime representing the first day of the month
    
    next_month
        this_month + 1 month
    
    last_month
        this_month - 1 month
    