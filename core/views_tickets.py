#Tickets views: list, create, delete
from django.shortcuts import render
from django.http import HttpResponse
from core import views_utils as utils
from core.models import Ticket,TicketForm, State, Department
from django.contrib.auth.models import User
#Needed for forms
from django.views.decorators.csrf import csrf_protect


def list_tickets(request):
	return render(request, 'tickets/list_tickets.html', {"site_vars": utils.site_vars()})


def create_ticket(request):
	#Status info
	status_info = State.objects.filter()
	dept_info = Department.objects.filter()
	users_info = User.objects.filter()

	#vars
	site_vars = utils.site_vars()
	status_info = status_info

	if request.method == 'POST':
		form = TicketForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = TicketForm()
	return render(request,'tickets/create_ticket.html', locals())