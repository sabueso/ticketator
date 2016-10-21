from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from core import views_utils as utils
from core.models import Ticket

# Create your views here.

@login_required
def index(request):
	#1-Test user
	#2-If admin
		#3-Obtain 10 last open tickets
		#4-Obtain 10 last in progress tickets
	#2-If user
		#3-Obtain 10 last open assigned tickets
		#4-Obtain 10 last in progress assigned tickets
	#3-Render RSS saved on settings
	return render(request, 'dashboard/dashboard.html')

@login_required
def settings(request):
	return render(request, 'settings/settings.html')