#Company views: list, create, delete

from core.models import Department, DepartmentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


#List tickets
def list_departments(request):
	department_list = Department.objects.all().order_by("-id")
	return render(request, 'departments/list_departments.html', locals())

def manage_department(request, department_id=None):
	#Try to locate the object to use it as an instance and if not, create a new one to use it in a new form.
	#common_data = common_ticket_data()
	if department_id:
		actual_department=get_object_or_404(Department,pk=department_id)
	else:
		actual_department=Department()
	#POST mode
	if request.method == 'POST':
		form = DepartmentForm(request.POST, instance=actual_department)
		if form.is_valid():
			form.save()
			return redirect("/settings/departments")
	else:
	#Non-POST mode, show only
		form = DepartmentForm(instance=actual_department)
	return render(request,'departments/create_edit_department.html', locals())


