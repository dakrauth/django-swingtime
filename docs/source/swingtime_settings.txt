:mod:`swingtime_settings` --- Configuration Settings
====================================================

.. module:: swingtime_settings


Settings
--------

Swingtime has it's settings module (:file:`conf/swingtime_settings.py`) that 
simulates how each Django project's :file:`setting.py` file functions. You can 
overwrite any or all of the configuration parameters described in 
:mod:`swingtime_settings` by creating a file in your own project and referencing
that file in your project settings using the name :data:`SWINGTIME_SETTINGS_MODULE`.

For example, from the demo's configuration::

    SWINGTIME_SETTINGS_MODULE = 'demo.swingtime_settings'


.. data:: TIMESLOT_TIME_FORMAT
 
    A "strftime" string for formatting start and end time selectors in forms.
    The default format is::
    
        '%I:%M %p'

.. data:: TIMESLOT_INTERVAL 

    Used for creating start and end time form selectors as well as time slot grids.
    Value should be ``datetime.timedelta`` value representing the incremental 
    differences between temporal options. The default is::
    
        ``datetime.timedelta(minutes=15)``

.. data:: TIMESLOT_START_TIME


    A datetime.time value indicting the starting time for time slot grids and form
    selectors. The default is::

        ``datetime.time(9)``

.. data:: TIMESLOT_END_TIME_DURATION 

    A ``datetime.timedelta`` value indicating the offset value from 
    ``TIMESLOT_START_TIME`` for creating time slot grids and form selectors. The 
    purpose for using a time delta is that it possible to span dates. For instance, 
    one could have a starting time of 3pm (15:00) and wish to indicate a ending value 
    1:30am (01:30), in which case a value of ``datetime.timedelta(hours=10.5)`` 
    could be specified to indicate that the 1:30 represents the following date's
    time and not the current date. Default::
    
        ``datetime.timedelta(hours=+8)``

.. data:: TIMESLOT_MIN_COLUMNS

    Indicates a minimum value (default: ``4``) for the number grid columns to be 
    shown in the time slot table.

.. data:: DEFAULT_OCCURRENCE_DURATION

    Indicate the default length in time for a new occurrence, specifed by using
    a ``datetime.timedelta`` object, defaulting to::

        ``datetime.timedelta(hours=+1)``

.. data:: CALENDAR_FIRST_WEEKDAY

    If not ``None``, passed to ``calendar.setfirstweekday`` function. 
    Default: ``6``
