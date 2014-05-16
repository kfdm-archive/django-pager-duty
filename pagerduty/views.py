from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

import requests
from requests.auth import AuthBase

from icalendar import Calendar


class PagerDutyAuth(AuthBase):
    def __call__(self, r):
        r.headers['Content-Type'] = 'application/json'
        r.headers['Authorization'] = 'Token token=' + settings.PAGERDUTY_API_KEY
        return r


class OnCallView(View):
    _URL = 'https://{0}.pagerduty.com/api/v1/escalation_policies/on_call'.format(
        settings.PAGERDUTY_SUBDOMAIN
    )

    def _parse_on_call(self):
        response = requests.get(self._URL, auth=PagerDutyAuth())
        response.raise_for_status()
        schedule = response.json()
        for policy in schedule['escalation_policies']:
            for on_call in policy['on_call']:
                if on_call['level'] != 1:
                    continue
                yield {
                    'start': on_call['start'],
                    'end': on_call['end'],
                    'userid': on_call['user']['id'],
                    'user': on_call['user']['name'],
                    'userlink': 'https://{0}.pagerduty.com/users/{1}'.format(
                        settings.PAGERDUTY_SUBDOMAIN,
                        on_call['user']['id']
                    ),
                    'policyid': policy['id'],
                    'policy': policy['name'],
                    'policylink': 'https://{0}.pagerduty.com/escalation_policies#{1}'.format(
                        settings.PAGERDUTY_SUBDOMAIN,
                        policy['id']
                    ),
                }

    def get(self, request):
        on_call = self._parse_on_call()
        return render(request, 'pagerduty_oncall.html', {
            'on_call': on_call,
        })


class CalendarView(View):
    _URL = "http://{0}.pagerduty.com/private/{1}/feed"
    _BLACKLIST = getattr(settings, 'PAGERDUTY_BLACKLIST', ())

    def get(self, request, api_key):
        url = self._URL.format(settings.PAGERDUTY_SUBDOMAIN, api_key)

        response = requests.get(url)
        response.raise_for_status()

        dest = Calendar()
        source = Calendar.from_ical(response.text)

        for key, value in source.items():
            dest.add(key, value)

        for event in source.subcomponents:
            if 'SUMMARY' in event and event['SUMMARY'] in self._BLACKLIST:
                continue
            dest.add_component(event)

        return HttpResponse(
            content=dest.to_ical(),
            content_type='text/plain; charset=utf-8'
        )
