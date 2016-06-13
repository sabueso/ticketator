#Tickets views: list, create, delete
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
#from core import views_utils as utils
from core.models import Ticket,TicketForm, State, Queue, Priority, Company, Rights
from django.contrib.auth.models import User, Group
#Needed for forms
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
#Rights magic
from core import rights
from django.db.models import Q



#Commond data & querys used to create/edit ticktes
def common_ticket_data():
	#Querys
	users_info = User.objects.all()
	queue_info = Queue.objects.all()
	comp_info =  Company.objects.all()
	status_info = State.objects.all()
	prio_info = Priority.objects.all()
	now_str = datetime.now()
	return {'status_info':status_info, 'prio_info':prio_info, \
	'queue_info':queue_info, 'users_info':users_info, 'now_str':now_str, 'comp_info':comp_info}

@login_required
#List tickets
def list_tickets(request, state_id=None):
	common_data = common_ticket_data()
	if request.user.username == 'admin':
		tickets_info = Ticket.objects.filter().order_by("-id")
	else:
		#queue is used in template to debug profits
		queues = rights.get_queues(request.user)
		if state_id:	
			tickets_info = Ticket.objects.filter(assigned_state=state_id).order_by("-id")
		else:
			tickets_info = Ticket.objects.filter(queues).order_by("-id")
	return render(request, 'tickets/list_tickets.html', locals())


#Create/Edit tickets
@login_required
def manage_ticket(request, ticket_id=None):
	#site_vars = utils.site_vars()
	#Common data
	common_data = common_ticket_data()
	if ticket_id:
		#Check if existis or raise 404	
		ticket_rights = rights.get_rights_for_ticket(user=request.user, queue=None, ticket_id=ticket_id)
		if ticket_rights.can_view == True :
			actual_ticket=get_object_or_404(Ticket,pk=ticket_id)
		else:
			raise Http404("You dont have enough permissions to see this ticket")
	else:
		#If not, assign a new ticket instance to be use as instance of form
		actual_ticket = Ticket()
	#POST mode
	if request.method == 'POST':
		form = TicketForm(request.POST, instance = actual_ticket , request=request)
		if form.is_valid():
			new_state_form = form.save(commit=False)
		 	new_state_form.create_user = request.user
		 	new_state_form.save()
		 	return redirect("/tickets")
	else:
	#Non-POST mode, show only
		form = TicketForm(instance=actual_ticket, request=request)
	return render(request,'tickets/create_edit_ticket.html', locals())
