from datetime import datetime, time, date
from dateutil import rrule

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .conf import swingtime_settings

__all__ = ("EventTypeBase", "EventManager", "EventBase", "OccurrenceManager", "OccurrenceBase")


def normalize_tz(dt):
    if isinstance(dt, (datetime, time)) and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.get_default_timezone())

    if isinstance(dt, date):
        return datetime.combine(dt, time(), tzinfo=timezone.get_default_timezone())

    return dt


class EventTypeBase(models.Model):
    """
    Simple ``Event`` classifcation.
    """

    abbr = models.CharField(_("abbreviation"), max_length=4, unique=True)
    label = models.CharField(_("label"), max_length=50)

    class Meta:
        verbose_name = _("event type")
        verbose_name_plural = _("event types")
        abstract = True

    def __str__(self):
        return self.label


class EventManager(models.Manager):
    def create_event_and_occurrences(
        self, title, event_type, description="", start_time=None, end_time=None, **rrule_params
    ):
        """
        Convenience function to create an ``Event``, optionally create an
        ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
        rules match those for ``Event.add_occurrences``.

        Returns the newly created ``Event`` instance.

        Parameters

        ``event_type``
            can be either an ``EventType`` object or 2-tuple of ``(abbreviation,label)``,
            from which an ``EventType`` is either created or retrieved.

        ``start_time``
            will default to the current hour if ``None``

        ``end_time``
            will default to ``start_time`` plus swingtime_settings.DEFAULT_OCCURRENCE_DURATION
            hour if ``None``

        ``freq``, ``count``, ``rrule_params``
            follow the ``dateutils`` API (see http://labix.org/python-dateutil)

        """

        if isinstance(event_type, dict):
            event_type = self.model.event_type.field.related_model.objects.get_or_create(
                abbr=event_type["abbr"], label=event_type["label"]
            )[0]

        event = self.create(title=title, description=description, event_type=event_type)
        start_time = start_time or timezone.now().replace(minute=0, second=0, microsecond=0)

        end_time = end_time or (start_time + swingtime_settings.DEFAULT_OCCURRENCE_DURATION)
        event.add_occurrences(start_time, end_time, **rrule_params)
        return event


class EventBase(models.Model):
    title = models.CharField(_("title"), max_length=32)
    description = models.CharField(_("description"), max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("swingtime:event", args=[str(self.pk)])

    def add_occurrences(self, start_time, end_time, **rrule_params):
        """
        Add one or more occurences to the event using a comparable API to
        ``dateutil.rrule``.

        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.

        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.

        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        """
        start_time = normalize_tz(start_time)
        end_time = normalize_tz(end_time)
        count = rrule_params.get("count")
        until = rrule_params.get("until")
        if until:
            until = rrule_params["until"] = normalize_tz(rrule_params.get("until"))

        if not (count or until):
            self.occurrence_set.create(start_time=start_time, end_time=end_time)
        else:
            rrule_params.setdefault("freq", rrule.DAILY)
            delta = end_time - start_time
            occurrences = [
                self.occurrence_set.model(start_time=ev, end_time=ev + delta, event=self)
                for ev in rrule.rrule(dtstart=start_time, **rrule_params)
            ]
            self.occurrence_set.bulk_create(occurrences)

    def upcoming_occurrences(self):
        """
        Return all occurrences that are set to start on or after the current
        time.
        """
        return self.occurrence_set.filter(start_time__gte=timezone.now())

    def next_occurrence(self):
        """
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        """
        return self.upcoming_occurrences().first()

    def daily_occurrences(self, dt=None):
        """
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        """
        return self.occurrence_set.daily_occurrences(dt=dt, event=self)


class OccurrenceManager(models.Manager):
    def daily_occurrences(self, dt=None, event=None):
        """
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        """
        dt = dt or timezone.now()
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            )
            | models.Q(
                end_time__gte=start,
                end_time__lte=end,
            )
            | models.Q(start_time__lt=start, end_time__gt=end)
        )

        return qs.filter(event=event) if event else qs


class OccurrenceBase(models.Model):
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))

    objects = OccurrenceManager()

    class Meta:
        abstract = True
        ordering = ["start_time"]

    def __str__(self):
        return "{}: {}".format(self.title, self.start_time.isoformat())

    def get_absolute_url(self):
        return reverse("swingtime:occurrence", args=[str(self.event.pk), str(self.pk)])

    def __lt__(self, other):
        return self.start_time < other.start_time

    @property
    def title(self):
        return self.event.title

    @property
    def event_type(self):
        return self.event.event_type
