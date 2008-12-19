================================
:mod:`forms` --- Swingtime Forms
================================

.. module:: forms

Convenience forms for adding and updating ``Event`` and ``Occurrence`` objects.

Functions
=========

``timeslot_options``
--------------------

.. function:: timeslot_options([interval=swingtime_settings.TIMESLOT_INTERVAL, start_time=swingtime_settings.TIMESLOT_START_TIME, end_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION, fmt=swingtime_settings.TIMESLOT_TIME_FORMAT])

    Create a list of time slot options for use in swingtime forms.
    
    The list is comprised of 2-tuples containing a 24-hour time value and a 
    12-hour temporal representation of that offset.

``timeslot_offset_options``
---------------------------

.. function:: timeslot_offset_options([interval=swingtime_settings.TIMESLOT_INTERVAL, start_time=swingtime_settings.TIMESLOT_START_TIME, end_delta=swingtime_settings.TIMESLOT_END_TIME_DURATION, fmt=swingtime_settings.TIMESLOT_TIME_FORMAT])

    Create a list of time slot options for use in swingtime forms.
    
    The list is comprised of 2-tuples containing the number of seconds since the
    start of the day and a 12-hour temporal representation of that offset.

Data
====

``default_timeslot_options``
----------------------------

.. data:: default_timeslot_options 

    defaults to ``timeslot_options()``

``default_timeslot_offset_options``
-----------------------------------

.. data:: default_timeslot_offset_options

    defaults to ``timeslot_offset_options()``


Classes
=======

``MultipleIntegerField``
------------------------

.. class:: MultipleIntegerField(django.forms.MultipleChoiceField)

    A form field for handling multiple integers.
    
    def __init__(self, choices, size=None, label=None, widget=None):
        if widget is None:
            widget = forms.SelectMultiple(attrs={'size' : size or len(choices)})


``SplitDateTimeWidget``
-----------------------

.. class:: SplitDateTimeWidget(django.forms.MultiWidget)

    A Widget that splits datetime input into a SelectDateWidget for dates and
    Select widget for times.

    .. method:: __init__(attrs=None)

        uses widgets ``SelectDateWidget`` and 
        ``forms.Select(choices=default_timeslot_options``

``MultipleOccurrenceForm``
--------------------------

.. class:: MultipleOccurrenceForm(django.forms.Form)

    .. attribute:: day

        forms.DateField
    
    .. attribute:: start_time_delta
    
        forms.IntegerField
    
    .. attribute:: end_time_delta
    
        forms.IntegerField

    .. attribute:: repeats
    
        forms.ChoiceField

    .. attribute:: count
    
        forms.IntegerField

    .. attribute:: until
    
        forms.DateField
    
    .. attribute:: freq
    
        forms.IntegerField

    .. attribute:: interval
    
        forms.IntegerField
    
    .. attribute:: week_days
    
        MultipleIntegerField
    
    .. attribute:: month_ordinal
    
        forms.IntegerField

    .. attribute:: month_ordinal_day
    
        forms.IntegerField

    .. attribute:: each_month_day = MultipleIntegerField(
    
    .. attribute:: year_months
    
        MultipleIntegerField
    
    .. attribute:: is_year_month_ordinal
        
        forms.BooleanField(required=False)
        
    .. attribute:: year_month_ordinal
    
        forms.IntegerField(widget=forms.Select(choices=ORDINAL))
        
    .. attribute:: year_month_ordinal_day
    
        forms.IntegerField(widget=forms.Select(choices=WEEKDAY_LONG))
    
    .. method:: __init__([*args, **kws])

        if ``initial`` contains ``dtstart`` - a ``datetime.datetime`` instance -
        the appropriate unspecified ``initial`` will be defaulted for the 
        form.

    .. method:: clean()
    
        populates ``cleaned_data`` with ``start_time`` and ``end_time`` values

    .. method:: save(event):

        Returns an ``Event`` object

``EventForm``
-------------

.. class:: EventForm(django.forms.ModelForm)

    A simple form for adding and updating Event attributes

``SingleOccurrenceForm``
------------------------

.. class:: SingleOccurrenceForm(django.forms.ModelForm)

    A simple form for adding and updating single Occurrence attributes

