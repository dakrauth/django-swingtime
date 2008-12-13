from django.contrib import admin
from swingtime.models import *

#===============================================================================
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('label', )


#===============================================================================
class NoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'created')


#===============================================================================
class OccurrenceInline(admin.TabularInline):
    model = Occurrence


#===============================================================================
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'description')
    list_filter = ('event_type', )
    inlines = [OccurrenceInline]


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Note, NoteAdmin)
