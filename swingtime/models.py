import importlib

from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _

from swingtime import base_models
from .conf import swingtime_settings, DEFAULT_SETTINGS

__all__ = (
    'Note',
    'EventType',
    'Event',
    'Occurrence',
    'create_event'
)

if swingtime_settings.NOTE_MODEL != DEFAULT_SETTINGS['NOTE_MODEL']:
    package, model = swingtime_settings.NOTE_MODEL.rsplit('.', 1)
    Note = getattr(importlib.import_module(package), model)
else:
    class Note(base_models.NoteBase):
        class Meta:
            app_label = 'swingtime'

if swingtime_settings.EVENT_MODEL != DEFAULT_SETTINGS['EVENT_MODEL']:
    package, model = swingtime_settings.EVENT_MODEL.rsplit('.', 1)
    Event = getattr(importlib.import_module(package), model)
else:
    class Event(base_models.EventBase):
        notes = GenericRelation(swingtime_settings.NOTE_MODEL, verbose_name=_('notes'))

        class Meta:
            app_label = 'swingtime'

if swingtime_settings.EVENT_TYPE_MODEL != DEFAULT_SETTINGS['EVENT_TYPE_MODEL']:
    package, model = swingtime_settings.EVENT_TYPE_MODEL.rsplit('.', 1)
    EventType = getattr(importlib.import_module(package), model)
else:
    class EventType(base_models.EventTypeBase):
        class Meta:
            app_label = 'swingtime'

if swingtime_settings.OCCURRENCE_MODEL != DEFAULT_SETTINGS['OCCURRENCE_MODEL']:
    package, model = swingtime_settings.OCCURRENCE_MODEL.rsplit('.', 1)
    Occurrence = getattr(importlib.import_module(package), model)
else:
    class Occurrence(base_models.OccurrenceBase):
        notes = GenericRelation(swingtime_settings.NOTE_MODEL, verbose_name=_('notes'))

        class Meta:
            app_label = 'swingtime'

create_event = base_models.event_creation_factory(Event, EventType)
