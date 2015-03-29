#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from pprint import pformat
from datetime import datetime, timedelta, date, time

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from dateutil import rrule
import swingtime
from swingtime import utils
from swingtime.models import *
from swingtime.forms import EventForm, MultipleOccurrenceForm

expected_table_1 = '''\
| 15:00 |          |          |          |          |          |
| 15:15 | zelda    |          |          |          |          |
| 15:30 | zelda    | alpha    |          |          |          |
| 15:45 |          | alpha    |          |          |          |
| 16:00 | bravo    | alpha    | foxtrot  |          |          |
| 16:15 | bravo    | alpha    | foxtrot  | charlie  |          |
| 16:30 | bravo    | alpha    | foxtrot  | charlie  | delta    |
| 16:45 |          | alpha    |          | charlie  | delta    |
| 17:00 |          | alpha    |          |          | delta    |
| 17:15 | echo     | alpha    |          |          |          |
| 17:30 | echo     | alpha    |          |          |          |
| 17:45 | echo     |          |          |          |          |
| 18:00 |          |          |          |          |          |
'''

expected_table_2 = '''\
| 15:30 | zelda    | alpha    |          |          |          |
| 15:45 |          | alpha    |          |          |          |
| 16:00 | bravo    | alpha    | foxtrot  |          |          |
| 16:15 | bravo    | alpha    | foxtrot  | charlie  |          |
| 16:30 | bravo    | alpha    | foxtrot  | charlie  | delta    |
| 16:45 |          | alpha    |          | charlie  | delta    |
| 17:00 |          | alpha    |          |          | delta    |
| 17:15 | echo     | alpha    |          |          |          |
| 17:30 | echo     | alpha    |          |          |          |
'''

expected_table_3 = '''\
| 16:00 | alpha    | bravo    | foxtrot  |          |          |
| 16:15 | alpha    | bravo    | foxtrot  | charlie  |          |
| 16:30 | alpha    | bravo    | foxtrot  | charlie  | delta    |
| 16:45 | alpha    |          |          | charlie  | delta    |
| 17:00 | alpha    |          |          |          | delta    |
| 17:15 | alpha    | echo     |          |          |          |
| 17:30 | alpha    | echo     |          |          |          |
'''

expected_table_4 = '''\
| 18:00 |          |          |          |          |
| 18:15 |          |          |          |          |
| 18:30 |          |          |          |          |
| 18:45 |          |          |          |          |
| 19:00 |          |          |          |          |
| 19:15 |          |          |          |          |
| 19:30 |          |          |          |          |
'''

expected_table_5 = '''\
| 16:30 | alpha    | bravo    | foxtrot  | charlie  | delta    |
'''

#===============================================================================
class TableTest(TestCase):

    fixtures = ['swingtime_test.json']

    #---------------------------------------------------------------------------
    def setUp(self):
        self._dt = dt = datetime(2008,12,11)

    #---------------------------------------------------------------------------
    def table_as_string(self, table):
        timefmt = '| {:<5s} '
        cellfmt = '| {:<8s} '
        out = []
        for tm, cells in table:
            out.append(timefmt.format(tm.strftime('%H:%M')))
            for cell in cells:
                if cell:
                    out.append(cellfmt.format(cell.event.title))
                else:
                    out.append(cellfmt.format(''))
            out.append('|\n')
            
        return ''.join(out)

    #---------------------------------------------------------------------------
    def _do_test(self, start, end, expect):
        start   = time(*start)
        dtstart = datetime.combine(self._dt, start)
        etd     = datetime.combine(self._dt, time(*end)) - dtstart
        table   = utils.create_timeslot_table(self._dt, start_time=start, end_time_delta=etd)
        actual  = self.table_as_string(table)
        out     = 'Expecting:\n{0}\nActual:\n{1}'.format(expect, actual)
        self.assertEqual(actual, expect, out)

    #---------------------------------------------------------------------------
    def test_slot_table_1(self):
        self._do_test((15,0), (18,0), expected_table_1)

    #---------------------------------------------------------------------------
    def test_slot_table_2(self):
        self._do_test((15,30), (17,30), expected_table_2)

    #---------------------------------------------------------------------------
    def test_slot_table_3(self):
        self._do_test((16,0), (17,30), expected_table_3)

    #---------------------------------------------------------------------------
    def test_slot_table_4(self):
        self._do_test((18,0), (19,30), expected_table_4)

    #---------------------------------------------------------------------------
    def test_slot_table_5(self):
        self._do_test((16,30), (16,30), expected_table_5)


#===============================================================================
class NewEventFormTest(TestCase):

    fixtures = ['swingtime_test']
    
    #---------------------------------------------------------------------------
    def test_new_event_simple(self):
        data = dict(
            title='QWERTY',
            event_type='1',
            day='2008-12-11',
            start_time_delta='28800',
            end_time_delta='29700',
            year_month_ordinal_day='2',
            month_ordinal_day='2',
            year_month_ordinal='1',
            month_option='each',
            count=2,
            repeats='count',
            freq='2',
            month_ordinal='1'
        )
        
        evt_form = EventForm(data)
        occ_form = MultipleOccurrenceForm(data)
        self.assertTrue(evt_form.is_valid(), evt_form.errors.as_text())
        self.assertTrue(occ_form.is_valid(), occ_form.errors.as_text())

        evt = occ_form.save(evt_form.save())
        self.assertEqual(evt.occurrence_set.count(), 2)
        
        self.assertEqual(
            occ_form.cleaned_data['start_time'],
            datetime(2008, 12, 11, 8),
            'Bad start_time: {0}'.format(pformat(occ_form.cleaned_data))
        )

    #---------------------------------------------------------------------------
    def test_freq(self):
        et = EventType.objects.get(pk=1)
        e = Event.objects.create(title='FIRE BAD!', description='***', event_type=et)
        dtstart = datetime(2015,2,12)
        data = dict(
            day=dtstart.date(),
            freq=rrule.MONTHLY,
            month_option='on',
            month_ordinal=1,
            month_ordinal_day=5,
            repeats='until',
            start_time_delta='28800',
            end_time_delta='29700',
            until=datetime(2015, 6, 10)
        )
        mof = MultipleOccurrenceForm(data, initial={'dtstart': dtstart})
        self.assertTrue(mof.is_valid(), mof.errors.as_text())

        mof.save(e)
        expected = [date(2015,m,d) for m,d in ((3, 6), (4, 3), (5, 1), (6, 5))]
        actual = [o.start_time.date() for o in e.occurrence_set.all()]
        self.assertEqual(expected, actual, '\nGOT:\n{}\n^\nEXP:\n{}'.format(pformat(actual), pformat(expected)))

#===============================================================================
class CreationTest(TestCase):
    
    #---------------------------------------------------------------------------
    def test_1(self):
        et = EventType.objects.create(abbr='foo', label='Foo')
        self.assertTrue(et.abbr == 'foo')
        
        e = Event.objects.create(title='Hello, world', description='Happy New Year', event_type=et)
        self.assertTrue(e.event_type == et)
        self.assertEqual(e.get_absolute_url(), '/events/{}/'.format(e.id))
        
        e.add_occurrences(datetime(2008,1,1), datetime(2008,1,1,1), freq=rrule.YEARLY, count=7)
        occs = list(e.occurrence_set.all())
        self.assertEqual(len(occs), 7)
        self.assertEqual(str(occs[0]), 'Hello, world: 2008-01-01T00:00:00')
        for i in range(7):
            o = occs[i]
            self.assertEqual(o.start_time.year, 2008 + i)
        
    #---------------------------------------------------------------------------
    def test_2(self):
        et = EventType.objects.create(abbr='bar', label='Bar')
        self.assertEqual(str(et), 'Bar')
        
        e = create_event('Bicycle repairman', event_type=et)
        self.assertEqual(str(e), 'Bicycle repairman')
        self.assertEqual(e.occurrence_set.count(), 1)
        self.assertEqual(e.daily_occurrences().count(), 1)
    
    #---------------------------------------------------------------------------
    def test_3(self):
        e = create_event(
            'Something completely different',
            event_type=('abbr', 'Abbreviation'),
            start_time=datetime(2008,12,1, 12),
            note='Here it is',
            freq=rrule.WEEKLY,
            byweekday=(rrule.TU, rrule.TH),
            until=datetime(2008,12,31)
        )
        self.assertIsInstance(e.event_type, EventType)
        self.assertEqual(e.event_type.abbr, 'abbr')
        self.assertEqual(str(e.notes.all()[0]), 'Here it is')
        occs = list(e.occurrence_set.all())
        for i, day in zip(range(len(occs)), [2, 4, 9, 11, 16, 18, 23, 25, 30]):
            o = occs[i]
            self.assertEqual(day, o.start_time.day)
    
    #---------------------------------------------------------------------------
    def test_4(self):
        e = create_event('This parrot has ceased to be!', ('blue', 'Blue'), count=3)
        occs = list(e.upcoming_occurrences())
        self.assertEqual(len(occs), 2)
        self.assertIsNotNone(e.next_occurrence())
        self.assertEqual(occs[1].title, 'This parrot has ceased to be!')

    def test_6(self):
        et = EventType.objects.create(abbr='foo', label='Foo')
        self.assertTrue(et.abbr == 'foo')
        
        e = Event.objects.create(title='Yet another event', description="with tons of occurrences", event_type=et)
        self.assertTrue(e.event_type == et)
        self.assertEqual(e.get_absolute_url(), '/events/{}/'.format(e.id))
        
        e.add_occurrences(datetime(2008,1,1), datetime(2008,1,1,1),
    			  freq=rrule.DAILY, until=datetime(2020,12,31)) # 
        occs = list(e.occurrence_set.all())
        self.assertEqual(len(occs), 4749)

#===============================================================================
class MiscTest(TestCase):
    
    #---------------------------------------------------------------------------
    def test_version(self):
        V = swingtime.VERSION
        self.assertEqual(swingtime.get_version(), '.'.join([str(i) for i in V]))
    
    #---------------------------------------------------------------------------
    def test_month_boundaries(self):
        dt = datetime(2012,2,15)
        start, end = utils.month_boundaries(dt)
        self.assertEqual(start, datetime(2012,2,1))
        self.assertEqual(end, datetime(2012,2,29))
    
