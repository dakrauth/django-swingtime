'''
#---------------------------------------------------------------------------------+
| Welcome to the swingtime demo project. This project's theme is a Karate dojo    |
| and the database will be pre-populated with some data relative to today's date. |
#---------------------------------------------------------------------------------+
'''
import os
import django
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, date, time, timedelta
from django.conf import settings
from django.db.models import signals
from django.utils.termcolors import make_style
from django.core.management.color import color_style
from dateutil import rrule
from swingtime import models as swingtime

class Term:
    info  = staticmethod(make_style(opts=('bold',), fg='green'))
    warn  = staticmethod(make_style(opts=('bold',), fg='yellow', bg='black'))
    error = staticmethod(make_style(opts=('bold',), fg='red', bg='black'))


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
    print(__doc__)
    print('Created event types: %s' % (
        ', '.join(['%s' % et for et in swingtime.EventType.objects.all()]),
    ))
    
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
    print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))
    
    # create an event with multiple occurrences by fixed count
    evt = swingtime.create_event(
        'Beginner Class',
        ets['bgn'],
        description='Open to all white and yellow belts',
        start_time=datetime.combine(now.date(), time(19)),
        count=30,
        byweekday=(rrule.MO, rrule.WE, rrule.FR)
    )
    print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

    # create an event with multiple occurrences by ending date (until)
    evt = swingtime.create_event(
        'Advance Class',
        ets['adv'],
        description='Open to all green and brown belts',
        start_time=datetime.combine(now.date(), time(18)),
        until=now + timedelta(days=+70),
        byweekday=(rrule.MO, rrule.WE, rrule.FR)
    )
    print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

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
    print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

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
    print('Created event "%s" with %d occurrences\n' % (evt, evt.occurrence_set.count()))


class Command(BaseCommand):
    help = 'Run the swingtime demo. If an existing demo database exists, it will recreated.'
    
    def handle(self, **options):
        dbpath = settings.DATABASES['default']['NAME']
        if os.path.exists(dbpath):
            self.stdout.write(Term.warn('Removing old database %s' % dbpath))
            os.remove(dbpath)
        self.stdout.write(Term.info('Creating database %s' % dbpath))

        call_command('migrate', no_input=True, interactive=False)
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        print('Done.\n\nCreating sample data...')
        create_sample_data()
        print('Done\n')

