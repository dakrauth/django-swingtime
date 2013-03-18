from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from karate import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='karate.html'), name='karate-home'),
    url(r'^swingtime/events/type/([^/]+)/$', views.event_type, name='karate-event'),
    (r'^swingtime/', include('swingtime.urls')),
)

