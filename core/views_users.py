#User views: list, create, delete

from django.shortcuts import render
from django.http import HttpResponse


def list_users(request):
	return HttpResponse("Listing users...")
