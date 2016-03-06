from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as settings_file

# Create your views here.

def site_name():
	site_vars = {}
	site_vars['name']=settings_file.SITE_NAME
	site_vars['version']=settings_file.SITE_VERSION
	return site_vars

def index(request):
	#return HttpResponse("<center>Dashboard place =>  Go to <a href=\"/tickets/\">tickets</a></center>")
	name = site_name()
	return render(request, 'dashboard/index.html', {"site_name": site_name()})