#Tickets views: list, create, delete

from django.shortcuts import render
from django.http import HttpResponse
from core import views_utils as utils


def list_tickets(request):
	return render(request, 'tickets/list_tickets.html', {"site_vars": utils.site_vars()})


def create_ticket(request):
	return render(request, 'tickets/create_ticket.html', {"site_vars": utils.site_vars()})