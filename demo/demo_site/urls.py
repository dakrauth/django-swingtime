import os
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

admin.autodiscover()
doc_root = os.path.join(os.path.dirname(settings.PROJECT_DIR), 'docs/build/html')

urlpatterns = patterns('',
    url(r'^$',               direct_to_template, { 'template': 'intro.html'}, name='demo-home'),
    (r'^karate/',            include('karate.urls')),
    (r'^admin/docs/',        include('django.contrib.admindocs.urls')),
    (r'^admin/',             include(admin.site.urls)),
    (r'^docs/?$',            redirect_to, dict(url='/docs/index.html')),
    (r'^docs/(?P<path>.*)$', serve, dict(document_root=doc_root, show_indexes=False))
)

if settings.DEBUG:
    data = dict(document_root=settings.MEDIA_ROOT, show_indexes=True)
    urlpatterns += patterns ('',
        (r'^media/(?P<path>.*)$', serve, data),
    )
