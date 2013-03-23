====================================================
:mod:`models` --- Swingtime Object Model Definitions
====================================================

.. module:: models

Functions
=========

``create_event``
----------------

.. function:: create_event(title, event_type [, description, start_time, end_time, note, **rrule_params])

    Convenience function to create an :class:`Event`, optionally create an 
    :class:`EventType`, and associated :class:`Occurrence` instances. 
    :class:`Occurrence` creation rules match those for :meth:`Event.add_occurrences`.
     
    Returns the newly created :class:`Event` instance.
    
    Parameters
    
    ``event_type``
        can be either an :class:`EventType` object or 2-tuple of ``(abbreviation,label)``, 
        from which an :class:`EventType` is either created or retrieved.

    ``description``
        sets the event's description if not ``None``
    
    ``start_time`` 
        will default to the current hour if ``None``
    
    ``end_time`` 
        will default to ``start_time`` plus :const:`swingtime_settings.DEFAULT_OCCURRENCE_DURATION`
        hour if ``None``
        
    ``note``
        if not ``None``, add a ``Note`` instance to the new event
    
    ``rrule_params``
        follows the ``dateutils`` API (see http://labix.org/python-dateutil)
    
    Example::
    
        from datetime import datetime, time
        from swingtime import models as swingtime
        from dateutil import rrule
        
        event = swingtime.create_event(
            'Beginner Class',
            ('bgn', 'Beginner Classes'),
            description='Open to all beginners',
            start_time=datetime.combine(datetime.now().date(), time(19)),
            count=6,
            byweekday=(rrule.MO, rrule.WE, rrule.FR)
        )
        
    

Classes
=======

``Note``
--------

.. class:: Note(django.db.models.Model)
    
    A generic model for adding simple, arbitrary notes to other models such as
    ``Event`` or ``Occurrence``.
    
    .. attribute:: note
    
        models.TextField
        
    .. attribute:: created
    
        models.DateTimeField


``EventType``
-------------

.. class:: EventType(django.db.models.Model)

    Simple ``Event`` classifcation.
    
    .. attribute:: abbr 
    
        models.CharField
        
    .. attribute:: label 
    
        models.CharField


``Event``
---------

.. class:: Event(django.db.models.Model)

    Container model for general metadata and associated ``Occurrence`` entries.

    .. attribute:: title 
    
        models.CharField
    
    .. attribute:: description 
    
        models.CharField
    
    .. attribute:: event_type 
    
        models.ForeignKey for ``EventType``
    
    .. attribute:: notes 
    
        generic.GenericRelation for ``Note``

    .. method:: get_absolute_url
    
        return ('swingtime-event', [str(self.id)])

    .. method:: add_occurrences(start_time, end_time [, **rrule_params])
    
        Add one or more occurences to the event using a comparable API to 
        ``dateutil.rrule``. 
        
        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.
        
        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.
        
        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.

    .. method:: upcoming_occurrences
        
        Return all occurrences that are set to start on or after the current
        time.

    .. method:: next_occurrence
        
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.

    .. method:: daily_occurrences([dt])
    
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.

``OccurrenceManager``
---------------------

.. class:: OccurrenceManager(models.Manager)
    
    .. method:: daily_occurrences([dt, event])
    
        Returns a queryset of for instances that have any overlap with a 
        particular day.
        
        Parameters
        
        ``dt``
            may be either a datetime.datetime, datetime.date object, or ``None``. 
            If ``None``, default to the current day
        
        ``event`` 
            can be an ``Event`` instance for further filtering


``Occurrence``
--------------

.. class:: Occurrence(django.db.models.Model)
    
    Represents the start end time for a specific occurrence of a master :class:`Event`
    object.

    .. attribute:: start_time 
    
        models.DateTimeField
        
    .. attribute:: end_time 
    
        models.DateTimeField
        
    .. attribute:: event
    
        models.ForeignKey - a non-editable Event object
        
    .. attribute:: notes
        
        generic.GenericRelation ``Note``

    .. method:: get_absolute_url
        
        'swingtime-occurrence', [str(self.event.id), str(self.id)])

    .. method:: __cmp__
    
        Compare two ``Occurrence`` start times

    .. attribute:: title
    
        Shortcut for the occurrence's ``Event.title``
        
    .. attribute:: event_type

        Shortcut for the occurrence's ``EventType``