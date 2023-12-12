from django.urls import re_path
from swingtime import views

urlpatterns = [
    re_path(r"^(?:calendar/)?$", views.today_view, name="swingtime-today"),
    re_path(
        r"^calendar/(?P<year>\d{4})/$", views.year_view, name="swingtime-yearly-view"
    ),
    re_path(
        r"^calendar/(\d{4})/(0?[1-9]|1[012])/$",
        views.month_view,
        name="swingtime-monthly-view",
    ),
    re_path(
        r"^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$",
        views.day_view,
        name="swingtime-daily-view",
    ),
    re_path(r"^events/$", views.event_listing, name="swingtime-events"),
    re_path(r"^events/add/$", views.add_event, name="swingtime-add-event"),
    re_path(r"^events/(\d+)/$", views.event_view, name="swingtime-event"),
    re_path(
        r"^events/(\d+)/(\d+)/$", views.occurrence_view, name="swingtime-occurrence"
    ),
]
