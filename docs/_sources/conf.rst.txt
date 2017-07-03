:mod:`conf` --- Configuration Settings
====================================================

.. module:: conf

Default Settings
----------------

You can override these defaults by creating ``dict`` named ``SWINGTIME`` in your
Django ``settings.py`` file. You only need to provide key/value pairs for the 
setting you wish to override. For Example::

    import datetime
    SWINGTIME = {'TIMESLOT_START_TIME': datetime.time(12, 30)}

All defaults::

    DEFAULTS = {

        # A "strftime" string for formatting start and end time selectors in forms.
        'TIMESLOT_TIME_FORMAT': '%I:%M %p',
     
        # Used for creating start and end time form selectors as well as time
        # slot grids. Value should be ``datetime.timedelta`` value representing
        # the incremental differences between temporal options.
        'TIMESLOT_INTERVAL': datetime.timedelta(minutes=15),

        # A datetime.time value indicting the starting time for time slot grids
        and form # selectors.
        'TIMESLOT_START_TIME': datetime.time(9),

        # A datetime.timedelta value indicating the offset value from 
        # TIMESLOT_START_TIME for creating time slot grids and form selectors.
        # The purpose for using a time delta is that it possible to span dates.
        # For instance, one could have a starting time of 3pm (15:00) and wish
        # to indicate a ending value # 1:30am (01:30), in which case a value of
        # datetime.timedelta(hours=10.5) # could be specified to indicate that
        # the 1:30 represents the following date's time and not the current date.
        'TIMESLOT_END_TIME_DURATION': datetime.timedelta(hours=+8),

        # Indicates a minimum value for the number grid columns to be shown in the
        # time slot table.
        'TIMESLOT_MIN_COLUMNS': 4,

        # Indicate the default length in time for a new occurrence,
        'DEFAULT_OCCURRENCE_DURATION': ``datetime.timedelta(hours=+1)``,

        # If not ``None``, passed to ``calendar.setfirstweekday`` function. 
        'CALENDAR_FIRST_WEEKDAY': 6
    }


