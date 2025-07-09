import datetime
import pytest
from django.urls import reverse
from django.forms.models import model_to_dict


@pytest.mark.django_db
class TestCBV:
    def test_listing(self, client):
        url = reverse("swingtime:events")
        r = client.get(url)
        assert r.status_code == 200

    def test_daily(self, client):
        url = reverse("swingtime:daily-view", kwargs={"year": 2018, "month": 3, "day": 18})
        r = client.get(url)
        assert r.status_code == 200

    def test_today(self, client):
        r = client.get(reverse("swingtime:today"))
        assert r.status_code == 200

    def test_month(self, client):
        url = reverse("swingtime:monthly-view", kwargs={"year": 2018, "month": 3})
        r = client.get(url)
        assert r.status_code == 200

    def test_current_month(self, client):
        url = reverse("swingtime:calendar")
        r = client.get(url)
        assert r.status_code == 200

    def test_year(self, client):
        url = reverse("swingtime:yearly-view", kwargs={"year": 2018})
        r = client.get(url)
        assert r.status_code == 200

    def test_event_view(self, client, occurence):
        url = reverse("swingtime:event", kwargs={"pk": occurence.event.id})
        r = client.get(url)
        assert r.status_code == 200

    def test_add_event_start_dtstart_bad(self, client):
        url = reverse("swingtime:add-event") + "?dtstart=BAD"
        r = client.get(url)
        assert r.status_code == 200

    def test_add_event_start_dtstart(self, client):
        r = client.get(reverse("swingtime:add-event") + "?dtstart=20180318")
        assert r.status_code == 200

    def test_add_event_start_no_dtstart(self, client):
        r = client.post(reverse("swingtime:add-event"))
        assert r.status_code == 200


class Foo:
    def test_event_view(self, client, occurence):
        # r'^events/(\d+)/$', views.event_view
        r = client.get(reverse("swingtime:event", kwargs={"pk": occurence.event.id}))
        assert r.status_code == 200

        r = client.post(
            reverse("swingtime:event", kwargs={"pk": occurence.event.id}),
            model_to_dict(occurence.event),
        )
        assert r.status_code == 400

        r = client.post(
            reverse("swingtime:event", kwargs={"pk": occurence.event.id}),
            dict(model_to_dict(occurence.event), _update=""),
        )
        assert r.status_code == 302

        r = client.post(
            reverse("swingtime:event", kwargs={"pk": occurence.event.id}),
            dict(model_to_dict(occurence.event), _add=""),
        )
        assert r.status_code == 200

        r = client.get(
            reverse(
                "swingtime:occurrence", kwargs={"event_pk": occurence.event.id, "pk": occurence.id}
            )
        )
        assert r.status_code == 200

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
            reverse(
                "swingtime:occurrence", kwargs={"event_pk": occurence.event.id, "pk": occurence.id}
            ),
            data,
        )
        assert r.status_code == 302
