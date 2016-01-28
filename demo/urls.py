import os
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()
doc_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs/build/html')

urlpatterns = [
    url(r'^$',                  TemplateView.as_view(template_name='intro.html'), name='demo-home'),
    url(r'^karate/',            include('karate.urls')),
    url(r'^admin/',             include(admin.site.urls)),
    url(r'^docs/?$',            RedirectView.as_view(url='/docs/index.html', permanent=True)),
    url(r'^docs/(?P<path>.*)$', serve, dict(document_root=doc_root, show_indexes=False))
]
