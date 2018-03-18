#!/usr/bin/env python
import pytest
from pprint import pformat
from datetime import datetime, timedelta, date, time
from dateutil import rrule
from django.urls import reverse
from django.forms.models import model_to_dict
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

@pytest.mark.django_db
class TestTable:

    @property
    def dt(self):
        return datetime(2008,12,11)

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

    def _do_test(self, start, end, expect):
        start   = time(*start)
        dtstart = datetime.combine(self.dt, start)
        etd     = datetime.combine(self.dt, time(*end)) - dtstart
        table   = utils.create_timeslot_table(self.dt, start_time=start, end_time_delta=etd)
        actual  = self.table_as_string(table)
        assert actual == expect

    def test_slot_table_1(self, events):
        self._do_test((15,0), (18,0), expected_table_1)

    def test_slot_table_2(self, events):
        self._do_test((15,30), (17,30), expected_table_2)

    def test_slot_table_3(self, events):
        self._do_test((16,0), (17,30), expected_table_3)
    
    def test_slot_table_4(self, events):
        self._do_test((18,0), (19,30), expected_table_4)
    
    def test_slot_table_5(self, events):
        self._do_test((16,30), (16,30), expected_table_5)


@pytest.mark.django_db
class TestNewEventForm:

    def test_new_event_simple(self, play_type):
        data = dict(
            title='QWERTY',
            event_type=play_type.id,
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
        assert True == evt_form.is_valid()
        assert '' == evt_form.errors.as_text()
        assert True == occ_form.is_valid()
        assert '' == occ_form.errors.as_text()

        evt = occ_form.save(evt_form.save())
        assert evt.occurrence_set.count() == 2
        assert occ_form.cleaned_data['start_time'] == datetime(2008, 12, 11, 8)
    
    def test_freq(self, play_type):
        e = Event.objects.create(title='FIRE BAD!', description='***', event_type=play_type)
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
        assert True == mof.is_valid()

        mof.save(e)
        expected = [date(2015,m,d) for m,d in ((3, 6), (4, 3), (5, 1), (6, 5))]
        actual = [o.start_time.date() for o in e.occurrence_set.all()]
        assert expected == actual

    def test_yearly(self, play_type):
        e = Event.objects.create(title='YEARLY', description='YYYY', event_type=play_type)
        dtstart = datetime(2018,3,18)
        data = dict(
            day=dtstart.date(),
            freq=rrule.YEARLY,
            year_months=['3'],
            repeats='count',
            count='3',
            month_option='each',
            start_time_delta='54000',
            end_time_delta='57600',
            is_year_month_ordinal = 'on',
            year_month_ordinal = '3',
            year_month_ordinal_day = '7',
        )
        mof = MultipleOccurrenceForm(data, initial={'dtstart': dtstart})
        assert True == mof.is_valid()

        mof.save(e)
        expected = [date(2018,3,18), date(2019,3,17), date(2020,3,15)]
        actual = [o.start_time.date() for o in e.occurrence_set.all()]
        assert expected == actual


@pytest.mark.django_db
class TestCreation:
    
    def test_1(self):
        et = EventType.objects.create(abbr='foo', label='Foo')
        assert et.abbr == 'foo'
        
        e = Event.objects.create(title='Hello, world', description='Happy New Year', event_type=et)
        assert e.event_type == et
        assert e.get_absolute_url() == '/events/{}/'.format(e.id)
        
        e.add_occurrences(datetime(2008,1,1), datetime(2008,1,1,1), freq=rrule.YEARLY, count=7)
        occs = list(e.occurrence_set.all())
        assert len(occs) == 7
        assert str(occs[0]) == 'Hello, world: 2008-01-01T00:00:00'
        for i in range(7):
            o = occs[i]
            assert o.start_time.year == 2008 + i
        
    def test_2(self):
        et = EventType.objects.create(abbr='bar', label='Bar')
        assert str(et) == 'Bar'
        
        e = create_event('Bicycle repairman', event_type=et)
        assert str(e) == 'Bicycle repairman'
        assert e.occurrence_set.count() == 1
        assert e.daily_occurrences().count() == 1
    
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
        assert True == isinstance(e.event_type, EventType)
        assert e.event_type.abbr == 'abbr'
        assert str(e.notes.all()[0]) == 'Here it is'
        occs = list(e.occurrence_set.all())
        for i, day in zip(range(len(occs)), [2, 4, 9, 11, 16, 18, 23, 25, 30]):
            o = occs[i]
            assert day == o.start_time.day
    
    
    def test_4(self):
        e = create_event('This parrot has ceased to be!', ('blue', 'Blue'), count=3)
        occs = list(e.upcoming_occurrences())
        assert len(occs) == 2
        assert e.next_occurrence() is not None
        assert occs[1].title == 'This parrot has ceased to be!'

    def test_6(self):
        et = EventType.objects.create(abbr='foo', label='Foo')
        assert et.abbr == 'foo'
        
        e = Event.objects.create(title='Yet another event', description="with tons of occurrences", event_type=et)
        assert e.event_type == et
        assert e.get_absolute_url() == '/events/{}/'.format(e.id)
        
        e.add_occurrences(
            datetime(2008,1,1),
            datetime(2008,1,1,1),
    		freq=rrule.DAILY,
            until=datetime(2020,12,31)
        )
        occs = list(e.occurrence_set.all())
        assert len(occs) == 4749


class TestMisc:
    
    def test_version(self):
        V = swingtime.VERSION
        assert swingtime.get_version() == '.'.join([str(i) for i in V])
    
    def test_month_boundaries(self):
        dt = datetime(2012,2,15)
        start, end = utils.month_boundaries(dt)
        assert start == datetime(2012,2,1)
        assert end == datetime(2012,2,29)
    

@pytest.mark.django_db
class TestViews:    

    def test_views(self, client, occurence):
        # r'^(?:calendar/)?$', views.today_view
        r = client.get(reverse('swingtime-today'))
        assert r.status_code == 200
        
        # r'^calendar/(?P<year>\d{4})/$', views.year_view
        r = client.get(reverse('swingtime-yearly-view', args=[2018]))
        assert r.status_code == 200
        
        # r'^calendar/(\d{4})/(0?[1-9]|1[012])/$', views.month_view
        r = client.get(reverse('swingtime-monthly-view', args=[2018, 3]))
        assert r.status_code == 200
        
        # r'^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', views.day_view
        r = client.get(reverse('swingtime-daily-view', args=[2018,3,18]))
        assert r.status_code == 200
        
        # r'^events/$', views.event_listing
        r = client.get(reverse('swingtime-events'))
        assert r.status_code == 200
        
        # r'^events/add/$', views.add_event
        r = client.get(reverse('swingtime-add-event') + '?dtstart=20180318')
        assert r.status_code == 200
        
        r = client.get(reverse('swingtime-add-event') + '?dtstart=BAD')
        assert r.status_code == 200

        r = client.post(reverse('swingtime-add-event'))
        assert r.status_code == 200

        # r'^events/(\d+)/$', views.event_view
        r = client.get(reverse('swingtime-event', args=[occurence.event.id]))
        assert r.status_code == 200

        r = client.post(
            reverse('swingtime-event', args=[occurence.event.id]),
            model_to_dict(occurence.event)
        )
        assert r.status_code == 400

        r = client.post(
            reverse('swingtime-event', args=[occurence.event.id]),
            dict(model_to_dict(occurence.event), _update='')
        )
        assert r.status_code == 302

        r = client.post(
            reverse('swingtime-event', args=[occurence.event.id]),
            dict(model_to_dict(occurence.event), _add='')
        )
        assert r.status_code == 200

        
        # r'^events/(\d+)/(\d+)/$', views.occurrence_view
        r = client.get(reverse('swingtime-occurrence', args=[
            occurence.event.id,
            occurence.id
        ]))
        assert r.status_code == 200

        # r'^events/(\d+)/(\d+)/$', views.occurrence_view
        start = occurence.start_time
        end = occurence.end_time

        data = {
            'end_time_0_day': end.day,
            'end_time_0_month': end.month,
            'end_time_0_year': end.year,
            'end_time_1': str(end.time()),
            'start_time_0_day': start.day,
            'start_time_0_month': start.month,
            'start_time_0_year': start.year,
            'start_time_1': str(start.time())
        }            
        r = client.post(reverse('swingtime-occurrence', args=[
            occurence.event.id,
            occurence.id
        ]), data)
        assert r.status_code == 302
