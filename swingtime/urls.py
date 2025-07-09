from django.urls import include, path, register_converter
from swingtime import views
from swingtime import utils

register_converter(utils.YearConverter, "yyyy")
register_converter(utils.MonthConverter, "mm")
register_converter(utils.DayConverter, "dd")

app_name = "swingtime"

calendar_patterns = [
    path("", views.CurrentMonthView.as_view(), name="calendar"),
    path("<yyyy:year>/", views.YearView.as_view(), name="yearly-view"),
    path("<yyyy:year>/<mm:month>/", views.MonthView.as_view(), name="monthly-view"),
    path("<yyyy:year>/<mm:month>/<dd:day>/", views.DayView.as_view(), name="daily-view"),
]

event_patterns = [
    path("", views.EventListView.as_view(), name="events"),
    path("create/", views.CreateEventView.as_view(), name="add-event"),
    path("<int:pk>/", views.EventView.as_view(), name="event"),
    path("<int:event_pk>/<int:pk>/", views.OccurrenceView.as_view(), name="occurrence"),
]

urlpatterns = [
    path("", views.TodayView.as_view(), name="today"),
    path("calendar/", include(calendar_patterns)),
    path("events/", include(event_patterns)),
]
