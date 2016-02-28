#Tickets views: list, create, delete

from django.shortcuts import render
from django.http import HttpResponse


def list_tickets(request):
	return HttpResponse("Listing tickets...")