# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from core.models import Ticket


def view_calendar(request):
    return render(request, 'core/calendar/calendar.html', {})


def get_events(request):
    if request.method == 'GET' and request.is_ajax():
        dict = []
        tickets = Ticket.objects.filter(assigned_user=request.user)

        for ticket in tickets:
            dict.append(ticket.events_as_json())
        return JsonResponse(dict, safe=False)
    else:
        return HttpResponse(status=405)
