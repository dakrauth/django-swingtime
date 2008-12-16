'''
================================================================================
Welcome to the django-swingtime demo project. This project's' is theme is a
Karate dojo and the database will be pre-populated with some data relative to
today's date. 
================================================================================
'''
from django.core.management import call_command
from django.core.management.base import NoArgsCommand
from datetime import datetime, date, time, timedelta
from django.conf import settings
from django.db.models import signals
from dateutil import rrule
from swingtime import models as swingtime


#-------------------------------------------------------------------------------
def create_sample_data():
    
    # Create the studio's event types
    ets = dict((
        (abbr, swingtime.EventType.objects.create(abbr=abbr, label=label))
        for abbr, label in (
            ('prv',  'Private Lesson'),
            ('bgn',  'Beginner Class'),
            ('adv',  'Advanced Class'),
            ('bbc',  'Black Belt Class'),
            ('spr',  'Sparring'),
            ('open', 'Open Dojo'),
            ('spc',  'Special Event'),
        )
    ))
    print __doc__
    print 'Created event types: %s' % (
        ', '.join(['%s' % et for et in swingtime.EventType.objects.all()]),
    )
    
    now = datetime.now()
    
    # create a single occurrence event
    evt = swingtime.create_event(
        'Grand Opening',
        ets['spc'],
        description='Open house',
        start_time=datetime.combine(now.date(), time(16)),
        end_time=datetime.combine(now.date(), time(18)),
        note='Free tea, sushi, and sake'
    )
    print 'Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count())
    
    # create an event with multiple occurrences by fixed count
    evt = swingtime.create_event(
        'Beginner Class',
        ets['bgn'],
        description='Open to all white and yellow belts',
        start_time=datetime.combine(now.date(), time(19)),
        count=30,
        byweekday=(rrule.MO, rrule.WE, rrule.FR)
    )
    print 'Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count())

    # create an event with multiple occurrences by ending date (until)
    evt = swingtime.create_event(
        'Advance Class',
        ets['adv'],
        description='Open to all green and brown belts',
        start_time=datetime.combine(now.date(), time(18)),
        until=now + timedelta(days=+70),
        byweekday=(rrule.MO, rrule.WE, rrule.FR)
    )
    print 'Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count())

    # create an event with multiple occurrences by fixed count on monthly basis
    evt = swingtime.create_event(
        'Black Belt Class',
        ets['bbc'],
        description='Open to all black belts',
        start_time=datetime.combine(now.date(), time(18, 30)),
        end_time=datetime.combine(now.date(), time(20, 30)),
        count=6,
        freq=rrule.MONTHLY,
        byweekday=(rrule.TH(+1), rrule.TH(+3))
    )
    print 'Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count())

    # create an event with multiple occurrences and alternate intervale
    evt = swingtime.create_event(
        'Open Dojo',
        ets['open'],
        description='Open to all students',
        start_time=datetime.combine(now.date(), time(12)),
        end_time=datetime.combine(now.date(), time(16)),
        interval=2,
        count=6,
        byweekday=(rrule.SU)
    )
    print 'Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count())
    print



#===============================================================================
class Command(NoArgsCommand):
    help = 'Run the swingtime demo. If an existing demo database exists, it will recreated.'
    
    #---------------------------------------------------------------------------
    def handle_noargs(self, **options):
        import os
        dbpath = os.path.join(settings.PROJECT_DIR, settings.DATABASE_NAME)
        if os.path.exists(dbpath):
            os.remove(dbpath)

        call_command('syncdb', noinput=True)
        create_sample_data()
        call_command('runserver')
        
