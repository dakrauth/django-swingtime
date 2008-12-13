from django.conf.urls.defaults import *

from swingtime import views

urlpatterns = patterns('',
    url(
        r'^(?:calendar/)?$', 
        views.view_today, 
        name='swingtime-today'
    ),

    url(
        r'^calendar/(\d{4})/$', 
        views.annual_view, 
        name='swingtime-annual-view'
    ),

    url(
        r'^calendar/(\d{4})/(0?[1-9]|1[012])/$', 
        views.monthly_view, 
        name='swingtime-monthly-view'
    ),

    url(
        r'^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', 
        views.daily_view, 
        name='swingtime-daily-view'
    ),

    url(
        r'^events/$',
        views.all_events,
        name='swingtime-events'
    ),
        
    url(
        r'^events/add/$', 
        views.add_event, 
        name='swingtime-add-event'
    ),
    
    url(
        r'^events/(\d+)/$', 
        views.view_event, 
        name='swingtime-event'
    ),
    
    url(
        r'^events/(\d+)/(\d+)/$', 
        views.view_occurrence, 
        name='swingtime-occurrence'
    ),
)
