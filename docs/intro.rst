============
Introduction
============

About Swingtime
===============

Welcome
-------

Swingtime is a `Django <http://www.djangoproject.com/>`_ application similar to
a stripped-down version of `iCal for Mac OS X <http://en.wikipedia.org/wiki/ICal>`_
or `Google Calendar <http://www.google.com/intl/en/googlecalendar/tour.html>`_.
Swingtime provides a :class:`~models.Event` model that acts as metadata container
for one or more :class:`~models.Occurrence` objects, which describe specific
start and end times.

Swingtime relies heavily upon both the ``datetime`` standard library package and
the ``dateutil`` package, featuring direct support for the ``dateutil.rrule`` 
interface to create occurrences.

A fairly simple example::

    >>> from datetime import *
    >>> from swingtime import models as swingtime
    >>> et = swingtime.EventType.objects.create(abbr='work', label='Work Related Events')
    >>> evt = swingtime.Event.objects.create(
    ...     title='New TPS Cover Sheet',
    ...     description='Kiss off, Lumbergh!',
    ...     event_type=et
    ... )
    >>> evt.add_occurrences(datetime(2013,4,1,16), datetime(2013,4,1,16,15), count=5)
    >>> for o in evt.occurrence_set.all():
    ...     print o
    ... 
    New TPS Cover Sheet: 2013-04-01T16:00:00
    New TPS Cover Sheet: 2013-04-02T16:00:00
    New TPS Cover Sheet: 2013-04-03T16:00:00
    New TPS Cover Sheet: 2013-04-04T16:00:00
    New TPS Cover Sheet: 2013-04-05T16:00:00

A bit more elaborate example, using the the convenience function :func:`models.create_event`::
    
    >>> # pay day is the last Friday of the month at 5pm
    >>> evt = swingtime.create_event(
    ...     'Pay day',
    ...     ('pay', 'Payroll'), # alternate means to add EventType on the fly
    ...     freq=rrule.MONTHLY,
    ...     byweekday=rrule.FR(-1),
    ...     until=datetime(2013,8,1),
    ...     start_time=datetime(2013,4,1,17)
    ... )
    >>> for o in evt.occurrence_set.all():
    ...     print o
    ... 
    Pay day: 2013-04-26T17:00:00
    Pay day: 2013-05-31T17:00:00
    Pay day: 2013-06-28T17:00:00
    Pay day: 2013-07-26T17:00:00
 

Features
--------

* Support for adding complex event occurrences via ``dateutil``
* Ready-made :class:`~forms.MultipleOccurrenceForm` for handling complex input
* Daily, monthly, and annual view functions
* Grid-based daily view generator, complete with alternating or sequential 
  :class:`~models.EventType` CSS-class handling
* Slightly better than average documentation, a few test cases, and commented code
* Active support (I have to eat my own dogfood)
* Built-in demo project / application

Requirements
------------

* `Django 1.7 <http://www.djangoproject.com/download/>`_
* Python 2.7
* The ``dateutil`` `package <http://labix.org/python-dateutil>`_.


Todo List
=========

* Add i18n support / translation support in demo
* Include a setup installer (I'm not doing ``easy_install``!)
* Add weekly view
* Import and export .ics files
* Add :class:`~models.Note` support to demo
* Add more tests
* Port over to github