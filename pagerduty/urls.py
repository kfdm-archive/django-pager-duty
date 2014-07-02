from django.conf.urls import patterns, url
from pagerduty.views import OnCallView, CalendarView, ReportView

urlpatterns = patterns(
    '',
    url(r'^$', OnCallView.as_view()),
    url(r'^report$', ReportView.as_view()),
    url(r'^(?P<api_key>\w+)\.ics$', CalendarView.as_view()),
)
