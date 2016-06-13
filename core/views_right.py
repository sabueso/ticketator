#Company views: list, create, delete

from core.models import Rights, RightForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


#List tickets
def list_rights(request):
	rights_list = Rights.objects.all().order_by('grp_src_id','-dpt_dst')
	return render(request, 'rights/list_rights.html', locals())

def manage_right(request, right_id=None):
	if right_id:
		actual_right=get_object_or_404(Rights,pk=right_id)
	else:
		actual_right=Rights()
	#POST mode
	if request.method == 'POST':
		form = RightForm(request.POST, instance=actual_right)
		if form.is_valid():		
			form.save()
			return redirect("/settings/rights")
	else:
	#Non-POST mode, show only
		form = RightForm(instance=actual_right)
	return render(request,'rights/create_edit_right.html', locals())

#some unusefull comment
#another one
