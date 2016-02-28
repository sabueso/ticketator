from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
	return HttpResponse("<center>Dashboard place =>  Go to <a href=\"/tickets/\">tickets</a></center>")
