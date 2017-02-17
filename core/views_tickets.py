#  -*- encoding: utf-8 -*-
from __future__ import unicode_literals

# Tickets views: list, create, delete
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Q

# from core import views_utils as utils
from core.models import Ticket, TicketForm, Attachment, AttachmentForm
from core.models import State, Queue, Priority, Company, Comments
from core.models import Logs, Microtasks
# Needed for forms
from datetime import datetime
# Rights magic
from core import rights
# Extending user model
from django.contrib.auth import get_user_model
# JSON for comments
import json
# Filtering data with multiple params

User = get_user_model()


# Commond data & querys used to create/edit ticktes
def common_ticket_data():
    # Querys
    users_info = User.objects.all()
    queue_info = Queue.objects.all()
    comp_info = Company.objects.all()
    status_info = State.objects.all()
    prio_info = Priority.objects.all()
    now_str = datetime.now()
    return {
        'status_info': status_info, 'prio_info': prio_info,
        'queue_info': queue_info, 'users_info': users_info,
        'now_str': now_str, 'comp_info': comp_info
    }


'''
list_tickets: list functions called in urls.py used to list tickets under /tickets url
'''


@login_required
def list_tickets(request, assigned_state=None):
    common_data = common_ticket_data()
    queues = rights.get_queues_as_q_for_ticket_model(request.user)
    states = State.objects.all()
    # We pass always granted_queues as a roundup to query_view requirements
    if not assigned_state:
        tickets = Ticket.objects.filter(queues) \
                                .filter(Q(assigned_state=2) | Q(assigned_state=1)) \
                                .order_by('-id')

    else:
        tickets = Ticket.objects.filter(queues) \
                                .filter(assigned_state=assigned_state) \
                                .order_by('-id')

    return render(request, 'tickets/list_tickets.html', locals())


@login_required
def delete_ticket(request, ticket_id=None):
    user_obj = request.user
    '''Check if we can add comment trought get_rights_for_ticket'''
    user_object_rights = rights.get_rights_for_ticket(
        user=user_obj, queue=None, ticket_id=ticket_id)
    if user_object_rights.can_delete:
        obj_to_delete = get_object_or_404(Ticket, pk=ticket_id)
        try:
            attach_to_delete = Attachment.objects.filter(ticket_rel=ticket_id)

        except Attachment.DoesNotExist:
            pass

        else:
            attach_to_delete.delete()
        obj_to_delete.delete()
        return redirect("/tickets")
    else:
        raise Http404("You dont have enough permissions to delete this ticket")


@login_required
def manage_ticket_dev(request, ticket_id=None):
    # site_vars = utils.site_vars()
    # Common data
    common_data = common_ticket_data()
    if ticket_id:
        # Check if existis or raise 404
        ticket_rights = rights.get_rights_for_ticket(
            user=request.user, queue=None, ticket_id=ticket_id)
        if ticket_rights.can_edit or request.user.is_superuser:
            actual_ticket = get_object_or_404(Ticket, pk=ticket_id)
            actual_files = Attachment.objects.filter(ticket_rel=ticket_id)
            actual_comments = Comments.objects.filter(ticket_rel=ticket_id).order_by('-id')
            actual_logs = Logs.objects.filter(log_ticket=ticket_id).order_by('-id')
            actual_microtasks = Microtasks.objects.filter(ticket_rel=ticket_id).order_by('-id')
        else:
            raise Http404("You dont have enough permissions to edit this ticket")
    else:
        # If not, assign a new ticket instance to be use as instance of form
        actual_ticket = Ticket()
    # POST mode
    if request.method == 'POST':
        form_ticket = TicketForm(
            request.POST, instance=actual_ticket, request=request, prefix="ticket")
        form_attach = AttachmentForm(request.POST, request.FILES, prefix="attach")
        if form_ticket.is_valid() and form_attach.is_valid():
            # The ticket part
            new_ticket_form = form_ticket.save(commit=False)
            new_ticket_form.create_user = request.user
            saved_ticket = new_ticket_form.save()
            # Seconf, save the attach part
            # instance = Attachment(
            # ticket_rel=new_ticket_form,file_name=request.FILES['attach-file_name'])
            # instance.save()
            if form_attach.has_changed():
                new_form_attach = form_attach.save(commit=False)
                new_form_attach.ticket_rel = new_ticket_form
                new_form_attach.save()
                if 'update-signal' in request.POST:
                    return redirect("/tickets/edit-dev/" + ticket_id + "")
                elif 'save-signal' in request.POST:
                    return redirect("/tickets")
            else:
                if 'save-signal' in request.POST:
                    return redirect("/tickets")
    else:
        # Non-POST mode, show only
        form_ticket = TicketForm(instance=actual_ticket, request=request, prefix="ticket")
        form_attach = AttachmentForm(instance=actual_ticket, prefix="attach")
    return render(request, 'tickets/create_edit_ticket.html', locals())


@login_required
def view_ticket(request, ticket_id=None):
    # Common data
    common_data = common_ticket_data()
    if ticket_id:
        # Check if existis or raise 404
        ticket_rights = rights.get_rights_for_ticket(
            user=request.user, queue=None, ticket_id=ticket_id)
        if ticket_rights.can_view:
            actual_ticket = get_object_or_404(Ticket, pk=ticket_id)
            actual_files = Attachment.objects.filter(ticket_rel=ticket_id)
            actual_comments = Comments.objects.filter(ticket_rel=ticket_id).order_by('-id')
            actual_logs = Logs.objects.filter(log_ticket=ticket_id).order_by('-id')
            actual_microtasks = Microtasks.objects.filter(ticket_rel=ticket_id).order_by('-id')
            if ticket_rights.can_edit or request.user.is_superuser:
                can_edit = True
            else:
                can_edit = False
        else:
            raise Http404("You dont have enough permissions to see this ticket")
    else:
        # If not, assign a new ticket instance to be use as instance of form
        raise Http404("No ticket selected")
    # POST mode

    form_ticket = TicketForm(instance=actual_ticket, request=request, prefix="ticket")
    form_attach = AttachmentForm(instance=actual_ticket, prefix="attach")
    return render(request, 'tickets/view.html', locals())


def save_comment(request, comment_data=None, private_data=None, ticket_data=None):
    # Save data
    inst_ticket = Ticket.objects.get(id=ticket_data)
    inst_data = Comments.objects.create(
        comment=comment_data, private=private_data, ticket_rel=inst_ticket, user_rel=request.user)
    inst_data.save()
    # # Log action
    # # logger(inst_ticket, request.user, "Add", "Comment")
    return "Comment saved"


def del_comment(request, message_id=None):
    msg_to_del = Comments.objects.get(id=message_id)
    msg_to_del.delete()
    return "Comment deleted"


# AJAX comments
@login_required
def add_comment_jx(request, ticket_id):
    if request.is_ajax() and request.POST:
        if request.POST.get('message_text'):
            '''Check if we can add comment trought get_rights_for_ticket'''
            user_object_rights = rights.get_rights_for_ticket(
                user=request.user, queue=None, ticket_id=ticket_id)
            if user_object_rights.can_comment or request.user.is_superuser:
                message_data = request.POST.get('message_text')
                status = save_comment(
                    request=request, comment_data=message_data, private_data=False,
                    ticket_data=ticket_id)
                data = {'message': "%s added" % status}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {'message': 'You don\'t have rights to comment'}
                response = HttpResponse(json.dumps(data), content_type='application/json')
                response.status_code = 400
                return response
    else:
        raise Http404

@login_required
def del_comment_jx(request):
    if request.is_ajax() and request.POST:
        if request.POST.get('message_id') and request.POST.get('ticket_id'):
            ticket_id = int(request.POST.get('ticket_id'))
            '''Check if we can add comment trought get_rights_for_ticket'''
            user_object_rights = rights.get_rights_for_ticket(
                user=request.user, queue=None, ticket_id=ticket_id)
            if user_object_rights.can_comment or request.user.is_superuser:
                message_data = request.POST.get('message_id')
                status = del_comment(request=request, message_id=message_data)
                data = {'message': "%s delete" % status}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {'message': 'You don\'t have rights to delete comment'}
                response = HttpResponse(json.dumps(data), content_type='application/json')
                response.status_code = 400
                return response

        data = {'message': "%s added" % status}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


def get_comments_jx(request, ticket_id=None):
    ''''
    As we comment in modules.py, in as_json function, serialize do not work with nested object
    so we construct that function to make
    As view here =>
    http://stackoverflow.com/questions/13031058/how-to-serialize-to-json-a-list-
    of-model-objects-in-django-python
    we can return all the data directly as a JSON an treat it in the ajax side
    '''
    qry = Comments.objects.filter(ticket_rel=ticket_id).order_by('-id')
    data = [ob.as_json(request) for ob in qry]
    return JsonResponse(data, safe=False)


def set_percentage_jx(request, ticket_id=None):
    if request.is_ajax() and request.POST:
        percentage_val = request.POST.get('range_value')
        if percentage_val:
            percent_update = Ticket.objects.get(pk=ticket_id)
            percent_update.percentage = percentage_val
            percent_update.save()
            data = {'message': "%s added" % percent_update}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


def get_percentage_jx(request, ticket_id=None):
    qry = Ticket.objects.get(id=ticket_id)
    data = qry.as_json()
    return JsonResponse(data, safe=False)


def save_microtask(
        request, subject_data=None, body_data=None, state_data=None, percentage_data=None,
        ticket_data=None):
    # Save data
    inst_ticket = Ticket.objects.get(id=ticket_data)
    inst_data = Microtasks.objects.create(
        ticket_rel=inst_ticket, assigned_state=state_data, subject=subject_data,
        body=body_data, percentage=percentage_data)
    inst_data.save()
    # # Log action
    # # logger(inst_ticket, request.user, "Add", "Comment")
    return "Microtask saved"


def update_microtask(
        request, subject_data=None, body_data=None, state_data=None, percentage_data=None,
        mk_data=None):
    # inst_data = Microtasks.objects.filter(id=mk_data).update(
    # assigned_state=state_data, subject=subject_data, body=body_data, percentage=percentage_data)
    inst_data = Microtasks.objects.get(id=mk_data)
    inst_data.assigned_state = state_data
    inst_data.subject = subject_data
    inst_data.body = body_data
    inst_data.percentage = percentage_data
    inst_data.save()
    return "Microtask saved"


def del_microtask(request, mk_id=None):
    mk_to_del = Microtasks.objects.get(id=mk_id)
    mk_to_del.delete()
    return "Microtask deleted"


# AJAX microtask
def add_microtask_jx(request, ticket_id=None):
    if request.is_ajax() and request.POST:
        '''if mk_id exists'''
        if request.POST.get('id_mk'):
            if (
                request.POST.get('subject_text') and request.POST.get('body_text') and
                    request.POST.get('state_id')):
                user_obj = request.user
                '''Check if we can add comment trought get_rights_for_ticket'''
                user_object_rights = rights.get_rights_for_ticket(
                    user=user_obj, queue=None, ticket_id=ticket_id)
                if user_object_rights.can_edit or request.user.is_superuser:
                    mk_clean = request.POST.get('id_mk')
                    subject_clean = request.POST.get('subject_text')
                    body_clean = request.POST.get('body_text')
                    state_clean = State.objects.get(id=int(request.POST.get('state_id')))
                    percentage_clean = request.POST.get('percentage_num')
                    status = update_microtask(
                        request=request, subject_data=subject_clean, body_data=body_clean,
                        state_data=state_clean, percentage_data=percentage_clean, mk_data=mk_clean)
                    data = {'message': "%s added" % status}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data = {'message': 'Some fields missing'}
                    response = HttpResponse(json.dumps(data), content_type='application/json')
                    response.status_code = 400
                    return response
            else:
                data = {'message': 'You don\'t have rights to comment'}
                response = HttpResponse(json.dumps(data), content_type='application/json')
                response.status_code = 400
                return response
        else:
            if (
                request.POST.get('subject_text') and request.POST.get('body_text') and
                    request.POST.get('state_id')):
                user_obj = request.user
                '''Check if we can add comment trought get_rights_for_ticket'''
                user_object_rights = rights.get_rights_for_ticket(
                    user=user_obj, queue=None, ticket_id=ticket_id)
                if user_object_rights.can_edit or request.user.is_superuser:
                    subject_clean = request.POST.get('subject_text')
                    body_clean = request.POST.get('body_text')
                    state_clean = State.objects.get(id=int(request.POST.get('state_id')))
                    percentage_clean = request.POST.get('percentage_num')
                    status = save_microtask(
                        request=request, subject_data=subject_clean, body_data=body_clean,
                        state_data=state_clean, percentage_data=percentage_clean,
                        ticket_data=ticket_id)
                    data = {'message': "%s added" % status}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data = {'message': 'Some fields missing'}
                    response = HttpResponse(json.dumps(data), content_type='application/json')
                    response.status_code = 400
                    return response
            else:
                data = {'message': 'You don\'t have rights to comment'}
                response = HttpResponse(json.dumps(data), content_type='application/json')
                response.status_code = 400
                return response
    else:
        raise Http404


def get_microtasks_jx(request, ticket_id=None):
    ''''
    As we comment in modules.py, in as_json function, serialize do not work with nested object
    so we construct that function to make
    As view here => http://stackoverflow.com/questions/13031058/how-to-serialize-
    to-json-a-list-of-model-objects-in-django-python
    we can return all the data directly as a JSON an treat it in the ajax side
    '''
    qry = Microtasks.objects.filter(ticket_rel=ticket_id).order_by('-id')
    data = [ob.as_json() for ob in qry]
    return JsonResponse(data, safe=False)


def del_microtask_jx(request, ticket_id=None):
    if request.is_ajax() and request.POST:
        if request.POST.get('mk_id'):
            user_obj = request.user
            '''Check if we can add comment trought get_rights_for_ticket'''
            user_object_rights = rights.get_rights_for_ticket(
                user=user_obj, queue=None, ticket_id=ticket_id)
            if user_object_rights.can_comment or request.user.is_superuser:
                mk_data = request.POST.get('mk_id')
                status = del_microtask(request=request, mk_id=mk_data)
                data = {'message': "%s delete" % status}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {'message': 'You don\'t have rights to delete comment'}
                response = HttpResponse(json.dumps(data), content_type='application/json')
                response.status_code = 400
                return response
        data = {'message': "%s deleted" % status}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


def get_microtask_jx(request, mk_id=None):
    qry = Microtasks.objects.get(id=mk_id)
    data = qry.as_json()
    return JsonResponse(data, safe=False)
