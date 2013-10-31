from datetime import datetime, date, timedelta

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from dateutil import rrule

__all__ = (
    'Note',
    'EventType',
    'Event',
    'Occurrence',
    'create_event'
)

#===============================================================================
class Note(models.Model):
    '''
    A generic model for adding simple, arbitrary notes to other models such as
    ``Event`` or ``Occurrence``.

    '''
    note = models.TextField(_('note'))
    created = models.DateTimeField(_('created'), auto_now_add=True)

    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    #===========================================================================
    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.note


#===============================================================================
class EventType(models.Model):
    '''
    Simple ``Event`` classifcation.

    '''
    abbr = models.CharField(_(u'abbreviation'), max_length=10, unique=True)
    label = models.CharField(_('label'), max_length=50)

    #===========================================================================
    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.label


#===============================================================================
class Event(models.Model):
    '''
    Container model for general metadata and associated ``Occurrence`` entries.
    '''
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    event_type = models.ForeignKey(EventType, verbose_name=_('event type'))
    notes = generic.GenericRelation(Note, verbose_name=_('notes'))

    #===========================================================================
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title', )

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title

    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        return ('swingtime-event', [str(self.id)])

    #---------------------------------------------------------------------------
    def add_occurrences(self, start_time, end_time, **rrule_params):
        '''
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
        '''
        rrule_params.setdefault('freq', rrule.DAILY)

        if 'count' not in rrule_params and 'until' not in rrule_params:
            self.occurrence_set.create(start_time=start_time, end_time=end_time)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                self.occurrence_set.create(start_time=ev, end_time=ev + delta)

    #---------------------------------------------------------------------------
    def upcoming_occurrences(self):
        '''
        Return all occurrences that are set to start on or after the current
        time.
        '''
        return self.occurrence_set.filter(start_time__gte=datetime.now())

    #---------------------------------------------------------------------------
    def next_occurrence(self):
        '''
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        '''
        upcoming = self.upcoming_occurrences()
        return upcoming and upcoming[0] or None

    #---------------------------------------------------------------------------
    def daily_occurrences(self, dt=None):
        '''
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        '''
        return Occurrence.objects.daily_occurrences(dt=dt, event=self)


#===============================================================================
class OccurrenceManager(models.Manager):

    use_for_related_fields = True

    #---------------------------------------------------------------------------
    def daily_occurrences(self, dt=None, event=None):
        '''
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.now()
        start = datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lte=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gt=end
            )
        )

        return qs.filter(event=event) if event else qs


#===============================================================================
class Occurrence(models.Model):
    '''
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    '''
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    event = models.ForeignKey(Event, verbose_name=_('event'), editable=False)
    notes = generic.GenericRelation(Note, verbose_name=_('notes'))

    objects = OccurrenceManager()

    #===========================================================================
    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrences')
        ordering = ('start_time', 'end_time')

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return u'%s: %s' % (self.title, self.start_time.isoformat())

    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        return ('swingtime-occurrence', [str(self.event.id), str(self.id)])

    #---------------------------------------------------------------------------
    def __cmp__(self, other):
        return cmp(self.start_time, other.start_time)

    #---------------------------------------------------------------------------
    @property
    def title(self):
        return self.event.title

    #---------------------------------------------------------------------------
    @property
    def event_type(self):
        return self.event.event_type


#-------------------------------------------------------------------------------
def create_event(
    title,
    event_type,
    description='',
    start_time=None,
    end_time=None,
    note=None,
    **rrule_params
):
    '''
    Convenience function to create an ``Event``, optionally create an
    ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
    rules match those for ``Event.add_occurrences``.

    Returns the newly created ``Event`` instance.

    Parameters

    ``event_type``
        can be either an ``EventType`` object or 2-tuple of ``(abbreviation,label)``,
        from which an ``EventType`` is either created or retrieved.

    ``start_time``
        will default to the current hour if ``None``

    ``end_time``
        will default to ``start_time`` plus swingtime_settings.DEFAULT_OCCURRENCE_DURATION
        hour if ``None``

    ``freq``, ``count``, ``rrule_params``
        follow the ``dateutils`` API (see http://labix.org/python-dateutil)

    '''
    from swingtime.conf import settings as swingtime_settings

    if isinstance(event_type, tuple):
        event_type, created = EventType.objects.get_or_create(
            abbr=event_type[0],
            label=event_type[1]
        )

    event = Event.objects.create(
        title=title,
        description=description,
        event_type=event_type
    )

    if note is not None:
        event.notes.create(note=note)

    start_time = start_time or datetime.now().replace(
        minute=0,
        second=0,
        microsecond=0
    )

    end_time = end_time or start_time + swingtime_settings.DEFAULT_OCCURRENCE_DURATION
    event.add_occurrences(start_time, end_time, **rrule_params)
    return event
