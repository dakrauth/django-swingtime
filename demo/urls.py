import os
from django import http
from django.contrib import admin
from django.views.static import serve
from django.urls import include, path
from django.views.generic import TemplateView
from . import views

doc_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs/")


def docs(request):
    return http.HttpResponsePermanentRedirect(os.path.join(request.path, "index.html"))


karate_patterns = [
    path("", TemplateView.as_view(template_name="karate.html"), name="karate-home"),
    path("swingtime/events/type/<str:abbr>/", views.event_type, name="karate-event"),
    path("swingtime/", include("swingtime.urls")),
]

urlpatterns = [
    path("", TemplateView.as_view(template_name="intro.html"), name="demo-home"),
    path("karate/", include(karate_patterns)),
    path("admin/", admin.site.urls),
    path("docs/", docs, name="swingtime-docs"),
    path("docs/<path:path>", serve, dict(document_root=doc_root, show_indexes=False)),
    path("smoketest/", views.smoketest),
]
