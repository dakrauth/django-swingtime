import pytest
from django.urls import reverse
from django.forms.models import model_to_dict


@pytest.mark.django_db
@pytest.mark.urls("swingtime.urls")
class TestFBV:
    def test_today(self, client):
        # r'^(?:calendar/)?$', views.today_view
        r = client.get(reverse("swingtime-today"))
        assert r.status_code == 200

    def test_year(self, client):
        # r'^calendar/(?P<year>\d{4})/$', views.year_view
        r = client.get(reverse("swingtime-yearly-view", args=[2018]))
        assert r.status_code == 200

    def test_month(self, client, occurence):
        # r'^calendar/(\d{4})/(0?[1-9]|1[012])/$', views.month_view
        url = reverse("swingtime-monthly-view", args=[2018, 3])
        r = client.get(url)
        assert r.status_code == 200

    def test_daily(self, client):
        # r'^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', views.day_view
        r = client.get(reverse("swingtime-daily-view", args=[2018, 3, 18]))
        assert r.status_code == 200

    def test_listing(self, client):
        # r'^events/$', views.event_listing
        url = reverse("swingtime-events")
        r = client.get(url)
        assert r.status_code == 200

    def test_add_event_start_dtstart(self, client):
        # r'^events/add/$', views.add_event
        r = client.get(reverse("swingtime-add-event") + "?dtstart=20180318")
        assert r.status_code == 200

    def test_add_event_start_dtstart_bad(self, client):
        r = client.get(reverse("swingtime-add-event") + "?dtstart=BAD")
        assert r.status_code == 200

    def test_add_event_start_no_dtstart(self, client):
        r = client.post(reverse("swingtime-add-event"))
        assert r.status_code == 200

    def test_event_view(self, client, occurence):
        # r'^events/(\d+)/$', views.event_view
        r = client.get(reverse("swingtime-event", args=[occurence.event.id]))
        assert r.status_code == 200

        r = client.post(
            reverse("swingtime-event", args=[occurence.event.id]), model_to_dict(occurence.event)
        )
        assert r.status_code == 400

        r = client.post(
            reverse("swingtime-event", args=[occurence.event.id]),
            dict(model_to_dict(occurence.event), _update=""),
        )
        assert r.status_code == 302

        r = client.post(
            reverse("swingtime-event", args=[occurence.event.id]),
            dict(model_to_dict(occurence.event), _add=""),
        )
        assert r.status_code == 200

        # r'^events/(\d+)/(\d+)/$', views.occurrence_view
        url = reverse("swingtime-occurrence", args=[occurence.event.id, occurence.id])
        r = client.get(url)
        assert r.status_code == 200

        # r'^events/(\d+)/(\d+)/$', views.occurrence_view
        start = occurence.start_time
        end = occurence.end_time

        data = {
            "end_time_0_day": end.day,
            "end_time_0_month": end.month,
            "end_time_0_year": end.year,
            "end_time_1": str(end.time()),
            "start_time_0_day": start.day,
            "start_time_0_month": start.month,
            "start_time_0_year": start.year,
            "start_time_1": str(start.time()),
        }
        r = client.post(
            reverse("swingtime-occurrence", args=[occurence.event.id, occurence.id]), data
        )
        assert r.status_code == 302
