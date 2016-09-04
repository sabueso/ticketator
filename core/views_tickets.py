#Tickets views: list, create, delete
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
#from core import views_utils as utils
from core.models import Ticket,TicketForm, Attachment, AttachmentForm, State, Queue, Priority, Company, Rights, Comments, Logs
from django.contrib.auth.models import User, Group
#Needed for forms
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
#Rights magic
from core import rights
from django.db.models import Q
#Extending user model
from django.contrib.auth import get_user_model
#JSON for comments
import json
#serialize is really working?
from django.core import serializers
#
from django.http import JsonResponse
#Filtering data with multiple params
from util import query_view
from core.views_logs import logger

User = get_user_model()


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
#def list_tickets(request, state_id=None, queue_id=None):
def list_tickets(request, **kwargs):
	common_data = common_ticket_data()
	queues = rights.get_queues_as_q_for_tickets(request.user)
	#We pass always granted_queues as a roundup to query_view requirements
	tickets_info = query_view(Ticket, request.GET, granted_queues = queues, **kwargs)
	return render(request, 'tickets/list_tickets.html', locals())

@login_required
def delete_ticket(request, ticket_id=None):
	obj_to_delete = get_object_or_404(Ticket,pk=ticket_id)
	try:
		attach_to_delete = Attachment.objects.filter(ticket_rel=ticket_id)
	except DoesNotExist:
		pass
	else:
		attach_to_delete.delete()
	obj_to_delete.delete()
	return redirect("/tickets")


@login_required
def manage_ticket_dev(request, ticket_id=None):
	#site_vars = utils.site_vars()
	#Common data
	common_data = common_ticket_data()
	if ticket_id:
		#Check if existis or raise 404	
		ticket_rights = rights.get_rights_for_ticket(user=request.user, queue=None, ticket_id=ticket_id)
		if ticket_rights.can_view == True :
			actual_ticket=get_object_or_404(Ticket,pk=ticket_id)
			actual_files=Attachment.objects.filter(ticket_rel=ticket_id)
			actual_comments=Comments.objects.filter(ticket_rel=ticket_id).order_by('-id')
			actual_logs=Logs.objects.filter(log_ticket=ticket_id).order_by('-id')
		else:
			raise Http404("You dont have enough permissions to see this ticket")
	else:
		#If not, assign a new ticket instance to be use as instance of form
		actual_ticket = Ticket()
	#POST mode
	if request.method == 'POST':
		form_ticket = TicketForm(request.POST, instance = actual_ticket , request=request, prefix="ticket")
		form_attach = AttachmentForm(request.POST, request.FILES, prefix="attach") 
		if form_ticket.is_valid() and form_attach.is_valid():
			#The ticket part
			new_ticket_form = form_ticket.save(commit=False)
		 	new_ticket_form.create_user = request.user
		 	saved_ticket = new_ticket_form.save()
		 	#Seconf, save the attach part
			#instance = Attachment(ticket_rel=new_ticket_form,file_name=request.FILES['attach-file_name'])
			#instance.save()
			if form_attach.has_changed():
				new_form_attach =  form_attach.save(commit=False)
				new_form_attach.ticket_rel = new_ticket_form
				new_form_attach.save()
				if 'update-signal' in request.POST:
					return redirect("/tickets/edit-dev/"+ticket_id+"")
				elif 'save-signal' in request.POST:
		 			return redirect("/tickets")
		 	else:
		 		if 'save-signal' in request.POST:
		 			return redirect("/tickets")
	else:
	#Non-POST mode, show only
		form_ticket = TicketForm(instance=actual_ticket, request=request, prefix="ticket")
		form_attach = AttachmentForm(instance=actual_ticket, prefix="attach")
	return render(request,'tickets/create_edit_ticket_dev.html', locals())

def save_comment(request, comment_data=None, private_data=None, ticket_data=None):
#Save data
	inst_ticket =  Ticket.objects.get(id=ticket_data)
	inst_data = Comments.objects.create(comment=comment_data, private=private_data, ticket_rel=inst_ticket, user_rel=request.user)
	inst_data.save()
##Log action
	##logger(inst_ticket, request.user, "Add", "Comment")
	return "Saved comment"

def del_comment(request, message_id=None):
	msg_to_del=Comments.objects.get(id=message_id)
	msg_to_del.delete()
	return "Deleted comment"

#AJAX comments
@login_required
def add_comment_jx(request, ticket_id=None):
	if request.is_ajax() and request.POST:
		if request.POST.get('message_text'):
			user_obj = request.user
			'''Check if we can add comment trought get_rights_for_ticket'''
			user_object_rights=rights.get_rights_for_ticket(user=user_obj, queue=None, ticket_id=ticket_id)
			if user_object_rights.can_comment == True:
				message_data=request.POST.get('message_text')
				status = save_comment(request=request, comment_data=message_data, private_data = False, ticket_data=ticket_id)
				data = {'message': "%s added" % status}
				return HttpResponse(json.dumps(data), content_type='application/json')
			else:
				data = {'message': 'You don\'t have rights to comment' }
				response = HttpResponse(json.dumps(data), content_type='application/json')
				response.status_code = 400
				return response
	else:
		raise Http404

@login_required
def del_comment_jx(request, ticket_id=None):
	if request.is_ajax() and request.POST:
		if request.POST.get('message_id'):
			user_obj = request.user
			'''Check if we can add comment trought get_rights_for_ticket'''
			user_object_rights=rights.get_rights_for_ticket(user=user_obj, queue=None, ticket_id=ticket_id)
			if user_object_rights.can_comment == True:
				message_data=request.POST.get('message_id')
				status = del_comment(request=request, message_id=message_data)
				data = {'message': "%s delete" % status}
				return HttpResponse(json.dumps(data), content_type='application/json')
			else:
				data = {'message': 'You don\'t have rights to delete comment' }
				response = HttpResponse(json.dumps(data), content_type='application/json')
				response.status_code = 400
				return response

			
		data = {'message': "%s added" % status}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404

@login_required
def get_comments_jx(request, ticket_id=None):
	''''
	As we comment in modules.py, in as_json function, serialize do not work with nested object
	so we construct that function to make 
	As view here => http://stackoverflow.com/questions/13031058/how-to-serialize-to-json-a-list-of-model-objects-in-django-python
	we can return all the data directly as a JSON an treat it in the ajax side
	'''
	qry =  Comments.objects.filter(ticket_rel=ticket_id).order_by('-id')
	data = [ob.as_json() for ob in qry]
	return JsonResponse(data, safe=False)


@login_required
def set_percentage_jx(request, ticket_id=None):
	if request.is_ajax() and request.POST:
		percentage_val = request.POST.get('range_value')
		if percentage_val:
			percent_update=Ticket.objects.get(pk=ticket_id)
			percent_update.percentage  = percentage_val
			percent_update.save()
			data = {'message': "%s added" % percent_update}
			return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404
