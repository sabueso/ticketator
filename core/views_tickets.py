#Tickets views: list, create, delete
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core import views_utils as utils
from core.models import Ticket,TicketForm, State, Department
from django.contrib.auth.models import User
#Needed for forms
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

#Commond data & querys used to create/edit ticktes
def common_ticket_data():
	#Querys
	status_info = State.objects.filter()
	dept_info = Department.objects.filter()
	users_info = User.objects.filter()
	now_str = datetime.now()
	return {'status_info':status_info, 'dept_info':dept_info, 'users_info':users_info, 'now_str':now_str }

#List tickets
def list_tickets(request):
	common_data = common_ticket_data()
	tickets_info = Ticket.objects.filter().order_by("-id")
	return render(request, 'tickets/list_tickets.html', locals())


#Add/Edit tickets
def manage_ticket(request, ticket_id=None):
	site_vars = utils.site_vars()
	#Common data
	common_data = common_ticket_data()
	if ticket_id:
		#Check if existis or raise 404	
		actual_ticket=get_object_or_404(Ticket,pk=ticket_id)
	else:
		#If not, assign a new ticket instance to be use as instance of form
		actual_ticket = Ticket()
	#POST mode
	if request.method == 'POST':
		form = TicketForm(request.POST, instance = actual_ticket)
		if form.is_valid():
			new_state_form = form.save(commit=False)
			new_state_form.create_user = request.user
			new_state_form.save()
			return redirect("/tickets")
	else:
	#Non-POST mode, show only
		form = TicketForm(instance=actual_ticket)
	return render(request,'tickets/create_ticket.html', locals())
