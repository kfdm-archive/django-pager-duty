from django.conf.urls import patterns
from pagerduty.views import OnCallView

urlpatterns = patterns(
    '',
    (r'^$', OnCallView.as_view()),
)
