# Tickets views: list, create, delete
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
# from core import views_utils as utils
from core.models import Ticket, TicketForm, Attachment, AttachmentForm, State
from core.models import Queue, Priority, Company
# Needed for forms
from datetime import datetime
# Rights magic
from core import rights
# Extending user model
from django.contrib.auth import get_user_model


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
        'queue_info': queue_info, 'users_info': users_info, 'now_str': now_str,
        'comp_info': comp_info}


@login_required
# List tickets
def list_tickets(request, state_id=None):
    common_data = common_ticket_data()
    if request.user.username == 'admin':
        tickets_info = Ticket.objects.filter().order_by("-id")
    else:
        # queue is used in template to debug profits
        queues = rights.get_queues(request.user)
        if state_id:
            tickets_info = Ticket.objects.filter(assigned_state=state_id).order_by("-id")
        else:
            tickets_info = Ticket.objects.filter(queues).order_by("-id")
    return render(request, 'tickets/list_tickets.html', locals())


# Create/Edit tickets
@login_required
def manage_ticket(request, ticket_id=None):
    # site_vars = utils.site_vars()
    # Common data
    common_data = common_ticket_data()
    if ticket_id:
        # Check if existis or raise 404
        ticket_rights = rights.get_rights_for_ticket(
            user=request.user, queue=None, ticket_id=ticket_id)
        if ticket_rights.can_view:
            actual_ticket = get_object_or_404(Ticket, pk=ticket_id)
            actual_files = Attachment.objects.filter(ticket_rel=ticket_id)
        else:
            raise Http404("You dont have enough permissions to see this ticket")
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
            # ticket_rel=new_ticket_form, file_name=request.FILES['attach-file_name'])
            # instance.save()
            if form_attach.has_changed():
                new_form_attach = form_attach.save(commit=False)
                new_form_attach.ticket_rel = new_ticket_form
                new_form_attach.save()
            return redirect("/tickets")
    else:
        # Non-POST mode, show only
        form_ticket = TicketForm(instance=actual_ticket, request=request, prefix="ticket")
        form_attach = AttachmentForm(instance=actual_ticket, prefix="attach")
    return render(request, 'tickets/create_edit_ticket_newui.html', locals())


@login_required
def delete_ticket(request, ticket_id=None):
    obj_to_delete = get_object_or_404(Ticket, pk=ticket_id)
    try:
        attach_to_delete = Attachment.objects.filter(ticket_rel=ticket_id)
    except Attachment.DoesNotExist:
        pass
    else:
        attach_to_delete.delete()
    obj_to_delete.delete()
    return redirect("/tickets")


# Jquery test version
@login_required
def manage_ticket_dev(request, ticket_id=None):
    # site_vars = utils.site_vars()
    # Common data
    common_data = common_ticket_data()
    if ticket_id:
        # Check if existis or raise 404
        ticket_rights = rights.get_rights_for_ticket(
            user=request.user, queue=None, ticket_id=ticket_id)
        if ticket_rights.can_view:
            actual_ticket = get_object_or_404(Ticket, pk=ticket_id)
            actual_files = Attachment.objects.filter(ticket_rel=ticket_id)
        else:
            raise Http404("You dont have enough permissions to see this ticket")
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
    return render(request, 'tickets/create_edit_ticket_dev.html', locals())
