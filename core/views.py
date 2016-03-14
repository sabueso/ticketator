from django.shortcuts import render
from django.http import HttpResponse
#from core import views_utils as utils

# Create your views here.

def index(request):
	return render(request, 'dashboard/index.html')

def settings(request):
	return render(request, 'dashboard/settings.html')