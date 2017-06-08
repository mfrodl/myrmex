from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^toggle/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.toggle, name='toggle'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.show, name='show'),
    url(r'^$', views.show, name='show'),
]
