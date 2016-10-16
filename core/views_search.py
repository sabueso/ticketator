from __future__ import unicode_literals
from core.models import Ticket
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from views_tickets import common_ticket_data
import operator

#List tickets
def main_search(request, state_id=None):
	common_data = common_ticket_data()
	if request.is_ajax() and request.POST:
		'''vars from post'''
		'''
		Some Q objects magic
		http://www.michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/
		'''
		subject_data=request.POST.get('subject_text')
		body_data=request.POST.get('body_text')
		if request.POST.get('assigned_id'):
			assigned_user_data=request.POST.get('assigned_id')
		else:
			assigned_user_data=None
		search_list=[Q(subject__contains = subject_data),\
					Q(body__contains = body_data),
					Q(assigned_user = assigned_user_data)]
		'''Admin results scope'''
		if request.user.is_superuser == True :
			qry_results = Ticket.objects.filter(reduce(operator.and_, search_list))
		else:
			pass
		data = [obj.as_json() for obj in qry_results]
		return JsonResponse(data, safe=False)
	return render(request, 'search/search_form.html', locals())