from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from core import views_utils as utils

# Create your views here.

@login_required
def index(request):
	return render(request, 'dashboard/dashboard.html')

@login_required
def settings(request):
	return render(request, 'settings/settings.html')