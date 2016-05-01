"""URLs for the ``calendarium`` app."""
from django.conf.urls import patterns, url

from calendarium.views import (
    CalendariumRedirectView,
    DayView,
    EventDetailView,
    MonthView,
    WeekView,
)


urlpatterns = patterns(
    '',
    # event views

    url(r'^event/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name='calendar_event_detail'),

    # calendar views
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        MonthView.as_view(),
        name='calendar_month'),

    url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
        WeekView.as_view(),
        name='calendar_week'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        DayView.as_view(),
        name='calendar_day'),

    url(r'^$',
        CalendariumRedirectView.as_view(),
        name='calendar_current_month'),

)
