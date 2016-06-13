#Company views: list, create, delete

from core.models import Queue, QueueForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


#List tickets
def list_queues(request):
	queue_list = Queue.objects.all().order_by("-id")
	return render(request, 'queues/list_queues.html', locals())

def manage_queue(request, queue_id=None):
	#Try to locate the object to use it as an instance and if not, create a new one to use it in a new form.
	#common_data = common_ticket_data()
	if queue_id:
		actual_queue=get_object_or_404(Queue,pk=queue_id)
	else:
		actual_queue=Queue()
	#POST mode
	if request.method == 'POST':
		form = QueueForm(request.POST, instance=actual_queue)
		if form.is_valid():
			form.save()
			return redirect("/settings/queue")
	else:
	#Non-POST mode, show only
		form = QueueForm(instance=actual_queue)
	return render(request,'queues/create_edit_queue.html', locals())


