from __future__ import unicode_literals
from core.models import Ticket
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from views_tickets import common_ticket_data
from django.contrib.auth import get_user_model


User = get_user_model()


# List tickets
def main_search(request, state_id=None):
    common_data = common_ticket_data()
    if request.is_ajax() and request.POST:
        '''vars from post'''
        '''
        Some Q objects magic
        http://www.michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/
        '''
        subject_data = request.POST.get('subject_text')
        body_data = request.POST.get('body_text')
        assigned_user_data = request.POST.get('assigned_id')
        creator_user_data = request.POST.get('creator_id')
        status_data = request.POST.get('status_id')

        '''Q config'''
        q_objects = Q()
        q_objects &= Q(subject__contains=subject_data)  # 'or' the Q objects together
        q_objects &= Q(body__contains=body_data)
        if assigned_user_data != '':
            q_objects &= Q(assigned_user__in=assigned_user_data)
        if creator_user_data != '':
            q_objects &= Q(create_user__in=creator_user_data)
        if status_data != '':
            q_objects &= Q(assigned_state__in=status_data)

        # Admin results scope'''
        if request.user.is_superuser:
            # qry_results = Ticket.objects.filter(reduce(operator.and_, q_objects))
            qry_results = Ticket.objects.filter(q_objects)
        else:
            pass
        data = [obj.as_json() for obj in qry_results]
        return JsonResponse(data, safe=False)

    return render(request, 'search/search_form.html', locals())
