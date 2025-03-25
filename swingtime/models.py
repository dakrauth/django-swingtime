from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from .conf import swingtime_settings
from . import base_models

__all__ = ("Note", "EventType", "Event", "Occurrence", "create_event")


class Note(models.Model):
    """
    A generic model for adding simple, arbitrary notes to other models such as
    ``Event`` or ``Occurrence``
    """

    note = models.TextField(_("note"))
    created = models.DateTimeField(_("created"), auto_now_add=True)
    content_type = models.ForeignKey(
        ContentType, verbose_name=_("content type"), on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")

    def __str__(self):
        return self.note


class EventType(base_models.EventTypeBase):
    """
    Simple ``Event`` classifcation.
    """

    pass


class Event(base_models.EventBase):
    """
    Container model for general metadata and associated ``Occurrence`` entries.
    """

    event_type = models.ForeignKey(
        EventType, verbose_name=_("event type"), on_delete=models.CASCADE
    )
    notes = GenericRelation(Note, verbose_name=_("notes"))

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ("title",)


class Occurrence(base_models.OccurrenceBase):
    """
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    """

    event = models.ForeignKey(
        Event, verbose_name=_("event"), editable=False, on_delete=models.CASCADE
    )
    notes = GenericRelation(Note, verbose_name=_("notes"))

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")
        ordering = ("start_time", "end_time")
        base_manager_name = "objects"


def create_event(
    title, event_type, description="", start_time=None, end_time=None, note=None, **rrule_params
):
    """
    Convenience function to create an ``Event``, optionally create an
    ``EventType``, and associated ``Occurrence`` objects. ``Occurrence`` creation
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

    if isinstance(event_type, tuple):
        event_type, created = EventType.objects.get_or_create(
            abbr=event_type[0], label=event_type[1]
        )

    event = Event.objects.create(title=title, description=description, event_type=event_type)

    if note is not None:
        event.notes.create(note=note)

    start_time = start_time or timezone.now().replace(minute=0, second=0, microsecond=0)

    end_time = end_time or (start_time + swingtime_settings.DEFAULT_OCCURRENCE_DURATION)
    event.add_occurrences(start_time, end_time, **rrule_params)
    return event
