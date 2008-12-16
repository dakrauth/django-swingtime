from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from karate import views

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { 'template': 'karate.html'}, name='karate-home'),
    url(r'^swingtime/events/type/([^/]+)/$', views.event_type, name='karate-event'),
    (r'^swingtime/', include('swingtime.urls')),
)

