from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { 'template': 'base.html'}, name="demo-home"),
    (r'^swingtime/', include('swingtime.urls')),
    (r'^admin/docs/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
