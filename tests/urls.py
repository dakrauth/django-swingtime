from django.conf.urls import include, url
urlpatterns = [
    url(r'^home/$', lambda request: None, name='demo-home'),
    url(r'^karate/$', lambda request: None, name='karate-home'),
    url(r'^', include('swingtime.urls')),
]
