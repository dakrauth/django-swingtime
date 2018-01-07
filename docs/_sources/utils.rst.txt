====================================
:mod:`utils` --- Swingtime Utilities
====================================

.. module:: utils

Common features and functions for swingtime

Functions
=========


``time_delta_total_seconds``
----------------------------

.. function:: time_delta_total_seconds(time_delta)

    Calculate the total number of seconds represented by a 
    ``datetime.timedelta`` object

``month_boundaries``
--------------------

.. function:: month_boundaries([dt=None])

    Return a 2-tuple containing the datetime instances for the first and last 
    dates of the current month or using ``dt`` as a reference. 
    

``css_class_cycler``
--------------------

.. function:: css_class_cycler()

    Return a dictionary keyed by :class:`~models.EventType` abbreviations, whose 
    values are an iterable or cycle of CSS class names.

``create_timeslot_table``
-------------------------

.. function:: create_timeslot_table([dt=None, items=None, start_time=swingtime_settings.TIMESLOT_START_TIME, end_time_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION, time_delta=swingtime_settings.TIMESLOT_INTERVAL, min_columns=swingtime_settings.TIMESLOT_MIN_COLUMNS, css_class_cycles=css_class_cycler, proxy_class=DefaultOccurrenceProxy])

    Create a grid-like object representing a sequence of times (rows) and 
    columns where cells are either empty or reference a wrapper object for 
    event occasions that overlap a specific time slot.
    
    Currently, there is an assumption that if an occurrence has a ``start_time`` 
    that falls with the temporal scope of the grid, then that ``start_time`` will
    also match an interval in the sequence of the computed row entries.
    
    ``dt``
        a ``datetime.datetime`` instance or ``None`` to default to now
    
    ``items``
        a queryset or sequence of :class:`~models.Occurrence` instances. If ``None``, 
        default to the daily occurrences for ``dt``
    
    ``start_time``
        a ``datetime.time`` instance, defaulting to 
        :const:`swingtime_settings.TIMESLOT_START_TIME` 
    
    ``end_time_delta``
        a ``datetime.timedelta`` instance, defaulting to 
        :const:`swingtime_settings.TIMESLOT_END_TIME_DURATION`
    
    ``time_delta``
        a ``datetime.timedelta`` instance, defaulting to 
        :const:`swingtime_settings.TIMESLOT_INTERVAL`

    ``min_column``
        the minimum number of columns to show in the table, defaulting to
        :const:`swingtime_settings.TIMESLOT_MIN_COLUMNS`
    
    ``css_class_cycles``
        if not ``None``, a callable returning a dictionary keyed by desired 
        :class:`EventType` abbreviations with values that iterate over progressive 
        CSS class names for the particular abbreviation; defaults to 
        :func:`css_class_cycler`
    
    ``proxy_class``
        a wrapper class for accessing an :class:`Occurrence` object, which 
        should also expose ``event_type`` and ``event_class`` attrs, and handle 
        the custom output via its __unicode__ method; defaults to 
        :class:`DefaultOccurrenceProxy`


Classes
=======

``BaseOccurrenceProxy``
-----------------------

.. class:: BaseOccurrenceProxy(object)

    A simple wrapper class for handling the representational aspects of an
    :class:`~models.Occurrence` instance.
    

``DefaultOccurrenceProxy``
--------------------------

.. class:: DefaultOccurrenceProxy(BaseOccurrenceProxy)

    Through the ``__unicode__`` method, outputs a **safe** string anchor tag
    for the :class:`~models.Occurrence` instance, followed by simple token placeholders
    to represent additional slot fillings.
