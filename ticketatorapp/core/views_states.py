# Company views: list, create, delete

from core.models import State, StateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


# List tickets
def list_state(request):
    if request.user.is_superuser:
        state_list = State.objects.all().order_by("-id")
        return render(request, 'states/list_states.html', locals())
    else:
        raise Http404


# Create or edit state
def manage_state(request, state_id=None):
    if request.user.is_superuser:
        # Try to locate the object to use it as an instance and if not, create a new one
        # to use it in a new form.
        # common_data = common_ticket_data()
        if state_id:
            actual_state = get_object_or_404(State, pk=state_id)
        else:
            actual_state = State()
        # POST mode
        if request.method == 'POST':
            form = StateForm(request.POST, instance=actual_state)
            if form.is_valid():
                form.save()
                return redirect("/settings/state")
        else:
            # Non-POST mode, show only
            form = StateForm(instance=actual_state)
        return render(request, 'states/create_edit_state.html', locals())
    else:
        raise Http404


# Delete state
def delete_state(request, state_id=None):
    if request.user.is_superuser:
        if state_id:
            actual_state = get_object_or_404(State, pk=state_id)
            actual_state.delete()
            return redirect("/settings/state")
    else:
        raise Http404
