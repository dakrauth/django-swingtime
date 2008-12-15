from datetime import datetime, date, timedelta

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from dateutil import rrule

#===============================================================================
class Note(models.Model):
    '''
    A generic model for adding simple, arbitrary notes to other models such as
    ``Event`` or ``Occurrence``.
    '''
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.note


#===============================================================================
class EventType(models.Model):
    '''
    Simple ``Event`` classifcation.
    '''
    abbr = models.CharField(verbose_name='Abbreviation', max_length=4, unique=True)
    label = models.CharField(max_length=50)

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.label


#===============================================================================
class Event(models.Model):
    '''
    Container model general metadata and associated ``Occurrence`` entries.
    '''
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    event_type = models.ForeignKey(EventType)
    notes = generic.GenericRelation(Note)

    #===========================================================================
    class Meta:
        ordering = ('title', )
        
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title

    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        return ('swingtime-event', [str(self.id)])

    #---------------------------------------------------------------------------
    def add_occurrences(self, dtstart, dtend, **rrule_params):
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
        ``dtstart`` and ``dtend`` values.
        '''
        rrule_params.setdefault('freq', rrule.DAILY)
        
        if 'count' not in rrule_params and 'until' not in rrule_params:
            self.occurrence_set.create(start_time=dtstart, end_time=dtend)
        else:
            delta = dtend - dtstart
            for ev in rrule.rrule(dtstart=dtstart, **rrule_params):
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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event = models.ForeignKey(Event, editable=False)
    notes = generic.GenericRelation(Note)

    objects = OccurrenceManager()

    #===========================================================================
    class Meta:
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
    
    * ``event_type`` can be either an ``EventType`` object or 2-tuple of
      (*abbreviation*,*label*), from which an ``EventType`` is either created or
      retrieved.
    * ``start_time`` will default to the current hour if ``None``
    * ``end_time`` will default to ``start_time`` plus 1 hour if ``None``
    * ``freq``, ``count``, and the ``rrule_params`` dict follow the ``dateutils``
      API (see http://labix.org/python-dateutil)
    
    '''
    
    if isinstance(event_type, tuple):
        event_type, created = EventType.objects.get_or_create(
            abbr=event_type[0],
            label=event_type[1]
        )
    
    start_time = start_time or datetime.now().replace(
        minutes=0,
        seconds=0, 
        microseconds=0
    )
    
    end_time = end_time or start_time + timedelta(hours=+1)
    
    event = Event.objects.create(
        title=title, 
        description=description,
        event_type=event_type
    )

    if note is not None:
        event.notes.create(note=note)
    
    event.add_occurrences(start_time, end_time, **rrule_params)
        
    return event
