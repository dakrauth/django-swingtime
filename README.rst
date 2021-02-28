Django Swingtime
================

.. image:: https://github.com/dakrauth/django-swingtime/workflows/Test/badge.svg
    :target: https://github.com/dakrauth/django-swingtime/actions

.. image:: https://badge.fury.io/py/django-swingtime.svg
    :target: http://badge.fury.io/py/django-swingtime

:Version: 1.2.1
:Demo: https://nerdfog.com/swingtime/
:Download: https://pypi.org/project/django-swingtime/
:Source: https://github.com/dakrauth/django-swingtime
:Documentation: http://dakrauth.github.io/django-swingtime/ 


Welcome
-------

Swingtime is a `Django <http://www.djangoproject.com/>`_ application similar to
a stripped-down version of iCal for Mac OS X or Google Calendar.

Swingtime provides a ``models.Event`` model that acts as metadata container
for one or more ``models.Occurrence`` objects, which describe specific
start and end times.

Swingtime relies heavily upon both the ``datetime`` standard library package and
the ``dateutil`` package, featuring direct support for the ``dateutil.rrule``
interface to create occurrences.

A fairly simple example:

.. code:: python

    >>> from datetime import *
    >>> from swingtime import models as swingtime
    >>> et = swingtime.EventType.objects.create(abbr='work', label='Work Related Events')
    >>> evt = swingtime.Event.objects.create(
    ...     title='New TPS Cover Sheet',
    ...     description='Kiss off, Lumbergh!',
    ...     event_type=et
    ... )
    >>> evt.add_occurrences(datetime(2018,3,18,16), datetime(2018,3,18,16,15), count=5)
    >>> for o in evt.occurrence_set.all():
    ...     print(o)
    ...
    New TPS Cover Sheet: 2018-03-18T16:00:00
    New TPS Cover Sheet: 2018-03-19T16:00:00
    New TPS Cover Sheet: 2018-03-20T16:00:00
    New TPS Cover Sheet: 2018-03-21T16:00:00
    New TPS Cover Sheet: 2018-03-22T16:00:00

A bit more elaborate example, using the the convenience function ``models.create_event``:

.. code:: python

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
    ...     print(o)
    ...
    Pay day: 2013-04-26T17:00:00
    Pay day: 2013-05-31T17:00:00
    Pay day: 2013-06-28T17:00:00
    Pay day: 2013-07-26T17:00:00

Demo
----

To view a demo, `click here <https://nerdfog.com/swingtime/>`_.

To run a local demo using Docker, do the following:

.. code:: bash

    $ docker build -t swingtime .
    $ docker run -p 8000:80 -d swingtime:latest

And browse to `localhost:8000 <http://localhost:8000>`_.


Features
--------

* Support for adding complex event occurrences via ``dateutil``
* Ready-made ``forms.MultipleOccurrenceForm`` for handling complex input
* Daily, monthly, and annual view functions
* Grid-based daily view generator, complete with alternating or sequential
  ``EventType`` CSS-class handling
* Slightly better than average documentation, a few test cases, and commented code
* Active support (I have to eat my own dogfood)
* Built-in demo project / application

Requirements
------------

* Python 3.6+
* `Django 2.2+ <http://www.djangoproject.com/download/>`_
* `python-dateutil <http://labix.org/python-dateutil>`_.

