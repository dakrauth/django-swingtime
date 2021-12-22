from django.urls import include, re_path
urlpatterns = [
    re_path(r'^home/$', lambda request: None, name='demo-home'),
    re_path(r'^karate/$', lambda request: None, name='karate-home'),
    re_path(r'^', include('swingtime.urls')),
]
