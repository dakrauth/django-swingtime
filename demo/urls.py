import os
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView

doc_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs/')

def docs(request):
    from django import http
    return http.HttpResponsePermanentRedirect(os.path.join(request.path, 'index.html'))


swingtime_patterns = [
    url(r'^$', TemplateView.as_view(template_name='intro.html'), name='demo-home'),
    url(r'^karate/', include('karate.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/$', docs, name='swingtime-docs'),
    url(r'^docs/(?P<path>.*)$', serve, dict(document_root=doc_root, show_indexes=False))
]

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/swingtime/')),
    url(r'^swingtime/', include(swingtime_patterns)),
]
