"""
Convenience forms for adding and updating ``Event`` and ``Occurrence``s.
"""

from django import forms
from swingtime.base_forms import (
    BaseMultipleOccurrenceForm,
    SplitDateTimeWidget,
    MultipleOccurrenceForm,
)

from .models import Event, Occurrence

__all__ = (
    "BaseMultipleOccurrenceForm",
    "SplitDateTimeWidget",
    "MultipleOccurrenceForm",
    "EventForm",
    "EventOccurrenceForm",
    "SingleOccurrenceForm",
)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.fields["description"].required = False


class EventOccurrenceForm(BaseMultipleOccurrenceForm, EventForm):
    def save(self):
        event = super().save()
        self.save_occurrences(event)
        return event


class SingleOccurrenceForm(forms.ModelForm):
    """
    A simple form for adding and updating single Occurrence attributes

    """

    start_time = forms.SplitDateTimeField(widget=SplitDateTimeWidget)
    end_time = forms.SplitDateTimeField(widget=SplitDateTimeWidget)

    class Meta:
        model = Occurrence
        fields = "__all__"
