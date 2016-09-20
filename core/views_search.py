from __future__ import unicode_literals
from core.models import Ticket
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

#List tickets
def main_search(request, state_id=None):
	if request.is_ajax() and request.POST:
		'''vars from post'''
		subject_data=request.POST.get('subject_text')
		'''Admin results scope'''
		if request.user.is_superuser == True :
			qry_results = Ticket.objects.filter(
				Q(subject__contains = subject_data)
				)
		data = [obj.as_json() for obj in qry_results]
		return JsonResponse(data, safe=False)
	return render(request, 'search/search_form.html', locals())