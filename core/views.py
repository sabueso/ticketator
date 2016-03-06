from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as settings_file

# Create your views here.

def site_vars():
	site_vars_data = {}
	site_vars_data['name']=settings_file.SITE_NAME
	site_vars_data['version']=settings_file.SITE_VERSION
	return site_vars_data

def index(request):
	#return HttpResponse("<center>Dashboard place =>  Go to <a href=\"/tickets/\">tickets</a></center>")
	return render(request, 'dashboard/index.html', {"site_vars": site_vars()})