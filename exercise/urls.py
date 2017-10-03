from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.show, name='show'),

    # TODO: This should return JSON with exercise for the month
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.show, name='show'),

    # HTML calendar for given month
    url(r'^calendar/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.calendar, name='calendar'),

    # Monthly exercise statistics
    url(r'^stats/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        views.stats, name='stats'),

    # Form submit handler
    url(r'^submit/$',
        views.submit, name='submit'),
]
