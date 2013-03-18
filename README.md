About Swingtime
===============

`Swingtime` is a [Django](http://www.djangoproject.com/) application similar to a
stripped-down version of iCal for Mac OS X or Google Calendar. `Swingtime` provides  an 
`Event` model that acts as a metadata container for one or more `Occurrence` objects,
which describe specific start and end times.

Swingtime relies heavily upon both the `datetime` standard library package and
the `dateutil` package, featuring direct support for the `dateutil.rrule`
interface to create occurrences.

A fairly simple example:

    >>> from datetime import *
    >>> from swingtime import models as swingtime
    >>> et = swingtime.EventType.objects.create(abbr='work', label='Work Related Events')
    >>> evt = swingtime.Event.objects.create(
    ...     title='New TPS Cover Sheet',
    ...     description='Kiss off, Lumbergh!',
    ...     event_type=et
    ... )
    >>> evt.add_occurrences(datetime(2008,12,1,16), datetime(2008,12,1,16,15), count=5)
    >>> for o in evt.occurrence_set.all():
    ...     print o
    ... 
    New TPS Cover Sheet: 2008-12-01T16:00:00
    New TPS Cover Sheet: 2008-12-02T16:00:00
    New TPS Cover Sheet: 2008-12-03T16:00:00
    New TPS Cover Sheet: 2008-12-04T16:00:00
    New TPS Cover Sheet: 2008-12-05T16:00:00

A bit more elaborate example, using the the convenience function `create_event`:
    
    >>> # pay day is the last Friday of the month at 5pm
    >>> evt = swingtime.create_event(
    ...     'Pay day',
    ...     ('pay', 'Payroll'), # alternate means to add EventType on the fly
    ...     freq=rrule.MONTHLY,
    ...     byweekday=rrule.FR(-1),
    ...     until=datetime(2009,4,1),
    ...     start_time=datetime(2008,12,25,17)
    ... )
    >>> for o in evt.occurrence_set.all():
    ...     print o
    ... 
    Pay day: 2008-12-26T17:00:00
    Pay day: 2009-01-30T17:00:00
    Pay day: 2009-02-27T17:00:00
    Pay day: 2009-03-27T17:00:00
 

Features
--------

* Support for adding complex event occurrences via `dateutil`
* Ready-made `MultipleOccurrenceForm` for handling complex input
* Daily, monthly, and annual view functions
* Grid-based daily view generator, complete with alternating or sequential 
  `EventType` CSS-class handling
* Slightly better than average documentation, a few test cases, and commented code
* Built-in demo project / application

Requirements
------------

* Django 1.4
* Python 2.7 
* [dateutil](http://labix.org/python-dateutil)

