import os
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()
doc_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs/build/html')

urlpatterns = patterns('',
    url(r'^$',               TemplateView.as_view(template_name='intro.html'), name='demo-home'),
    (r'^karate/',            include('karate.urls')),
    (r'^admin/',             include(admin.site.urls)),
    (r'^docs/?$',            RedirectView.as_view(url='/docs/index.html')),
    (r'^docs/(?P<path>.*)$', serve, dict(document_root=doc_root, show_indexes=False))
)
