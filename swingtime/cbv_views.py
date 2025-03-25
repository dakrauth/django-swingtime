import logging
import calendar
import itertools
from functools import cached_property, partial
from datetime import datetime, timedelta
from django.db import models
from dateutil import parser
from django.utils import timezone
from vanilla import TemplateView, ListView, CreateView, UpdateView

from .conf import swingtime_settings
from . import utils

logger = logging.getLogger("swingtime")


if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


class SwingtimeImportMixin:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if name == "model" and isinstance(value, str):
            value = self.model = self.__class__.model = utils.cached_import(value)
        elif name == "form_class" and isinstance(value, str):
            value = self.form = self.__class__.form = utils.cached_import(value)

        return value


class EventListView(SwingtimeImportMixin, ListView):
    context_object_name = "events"
    template_name = "swingtime/event_list.html"
    model = swingtime_settings.EVENT_LIST_VIEW_MODEL


class DayView(TemplateView):
    template_name = "swingtime/daily_view.html"
    occurrence_cls = swingtime_settings.DAY_VIEW_OCCURRENCE_CLS
    event_type_cls = swingtime_settings.DAY_VIEW_EVENT_TYPE_CLS

    def get_day(self):
        return datetime(
            self.kwargs["year"],
            self.kwargs["month"],
            self.kwargs["day"],
            tzinfo=timezone.get_default_timezone(),
        )

    def get_timeslots(self, day):
        return utils.create_timeslot_table(
            day, self.get_timeslot_items(), **self.get_timeslot_params()
        )

    def get_timeslot_items(self):
        return None

    def get_timeslot_params(self):
        return {
            "occurrence_cls": utils.cached_import(self.occurrence_cls),
            "css_class_cycles": partial(
                utils.css_class_cycler, event_type_cls=utils.cached_import(self.event_type_cls)
            ),
        }

    def get_context_data(self, **kwargs):
        day = self.get_day()
        timeslots = self.get_timeslots(day)
        return super().get_context_data(
            day=day,
            next_day=day + timedelta(days=+1),
            prev_day=day + timedelta(days=-1),
            timeslots=timeslots,
            **kwargs,
        )


class TodayView(DayView):
    def get_day(self):
        return timezone.localtime()


class MonthView(SwingtimeImportMixin, ListView):
    template_name = "swingtime/monthly_view.html"
    model = swingtime_settings.MONTH_VIEW_MODEL

    def get_queryset(self):
        queryset = self.model.objects.filter(
            start_time__year=self.kwargs["year"], start_time__month=self.kwargs["month"]
        )
        return queryset.select_related()

    def get_month(self):
        return datetime(self.kwargs["year"], self.kwargs["month"], 1)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        dtstart = self.get_month()
        cal = calendar.monthcalendar(dtstart.year, dtstart.month)
        last_day = max(cal[-1])
        tz = timezone.get_default_timezone()

        def start_day(o):
            return o.start_time.astimezone(tz).day

        occurrences = kwargs["object_list"]
        by_day = {dt: list(o) for dt, o in itertools.groupby(occurrences, start_day)}
        cal_list = [[(d, by_day.get(d, [])) for d in row] for row in cal]
        kwargs.update(
            today=timezone.localtime(),
            calendar=cal_list,
            this_month=dtstart,
            next_month=dtstart + timedelta(days=+last_day),
            last_month=dtstart + timedelta(days=-1),
        )
        return kwargs


class CurrentMonthView(MonthView):
    def get_queryset(self):
        now = self.now
        queryset = self.model.objects.filter(start_time__year=now.year, start_time__month=now.year)
        return queryset.select_related()

    def get_month(self):
        now = self.now
        return datetime(now.year, now.month, 1)

    @cached_property
    def now(self):
        return timezone.localtime()


class YearView(SwingtimeImportMixin, ListView):
    template_name = "swingtime/yearly_view.html"
    model = swingtime_settings.YEAR_VIEW_MODEL

    def get_queryset(self):
        year = self.kwargs["year"]
        return self.model.objects.filter(
            models.Q(start_time__year=year) | models.Q(end_time__year=year)
        ).select_related()

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        year = self.kwargs["year"]

        def group_key(o):
            return datetime(
                year,
                o.start_time.month if o.start_time.year == year else o.end_time.month,
                1,
            )

        occurrences = kwargs["object_list"]
        kwargs.update(
            year=year,
            by_month=[(dt, list(o)) for dt, o in itertools.groupby(occurrences, group_key)],
            next_year=year + 1,
            last_year=year - 1,
        )
        return kwargs


class CreateEventView(SwingtimeImportMixin, CreateView):
    template_name = "swingtime/add_event.html"
    model = swingtime_settings.CREATE_EVENT_VIEW_MODEL
    form_class = swingtime_settings.CREATE_EVENT_VIEW_FORM

    def get_form(self, data=None, files=None, **kwargs):
        dtstart = self.request.GET.get("dtstart")
        if dtstart:
            try:
                parser.parse(dtstart)
            except (TypeError, ValueError):
                dtstart = None
                logger.debug(f"Invalid dtstart parameter 'dtstart': {dtstart}")
            else:
                kwargs.setdefault("initial", {})["dtstart"] = dtstart

        cls = self.get_form_class()
        return cls(data=data, files=files, **kwargs)


class EventView(SwingtimeImportMixin, UpdateView):
    template_name = "swingtime/event_detail.html"
    model = swingtime_settings.EVENT_VIEW_MODEL
    form_class = swingtime_settings.EVENT_VIEW_FORM


class OccurrenceView(SwingtimeImportMixin, UpdateView):
    template_name = "swingtime/occurrence_detail.html"
    model = swingtime_settings.OCCURRENCE_VIEW_MODEL
    form_class = swingtime_settings.OCCURRENCE_VIEW_FORM
