#Company views: list, create, delete

from django.contrib.auth.models import Group
from core.models import GroupForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


#List tickets
def list_groups(request):
	group_list = Group.objects.all().order_by("-id")
	return render(request, 'groups/list_groups.html', locals())

def manage_group(request, group_id=None):
	if group_id:
		actual_group=get_object_or_404(Group,pk=group_id)
	else:
		actual_group=Group()
	#POST mode
	if request.method == 'POST':
		form = GroupForm(request.POST, instance=actual_group)
		if form.is_valid():
			form.save()
			return redirect("/settings/groups")
	else:
	#Non-POST mode, show only
		form = GroupForm(instance=actual_group)
	return render(request,'groups/create_edit_group.html', locals())


