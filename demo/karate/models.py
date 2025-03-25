from django.db import models
from swingtime import base_models

__all__ = ("EventType", "Event", "Occurrence")


class EventType(base_models.EventTypeBase):
    pass


class Event(base_models.EventBase):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)

    class Meta:
        ordering = ("title",)


class Occurrence(base_models.OccurrenceBase):
    event = models.ForeignKey(Event, editable=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ("start_time", "end_time")
        base_manager_name = "objects"
