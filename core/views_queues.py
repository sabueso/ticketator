# Company views: list, create, delete

from core.models import Queue, QueueForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


# List tickets
def list_queues(request):
    if request.user.is_superuser:
        queue_list = Queue.objects.all().order_by("-id")
    else:
        raise Http404
    return render(request, 'queues/list_queues.html', locals())


def manage_queue(request, queue_id=None):
    # Try to locate the object to use it as an instance and if not, create a new one to use it
    # in a new form.
    # common_data = common_ticket_data()
    if request.user.is_superuser:
        if queue_id:
            actual_queue = get_object_or_404(Queue, pk=queue_id)
        else:
            actual_queue = Queue()
        # POST mode
        if request.method == 'POST':
            form = QueueForm(request.POST, instance=actual_queue)
            if form.is_valid():
                form.save()
                return redirect("/settings/queue")
        else:
            # Non-POST mode, show only
            form = QueueForm(instance=actual_queue)
        return render(request, 'queues/create_edit_queue.html', locals())
    else:
        raise Http404


# Delete state
def delete_queue(request, queue_id=None):
    if request.user.is_superuser:
        if queue_id:
            actual_queue = get_object_or_404(Queue, pk=queue_id)
            actual_queue.delete()
            return redirect("/settings/queue")
    else:
        raise Http404
