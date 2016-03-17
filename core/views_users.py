#User views: list, create, delete
from django.contrib.auth.models import User
from core.models import UserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse


#List tickets
def list_users(request, state_id=None):
	user_list = User.objects.all().order_by("-id")
	return render(request, 'users/list_users.html', locals())

def manage_user(request, user_id=None):
	#Try to locate the object to use it as an instance and if not, create a new one to use it in a new form.
	#common_data = common_ticket_data()
	if user_id:
		actual_user=get_object_or_404(User,pk=user_id)
	else:
		actual_user = User()
	#POST mode
	if request.method == 'POST':
		form = UserForm(request.POST, instance=actual_user)
		if form.is_valid():
			#form.check_password()
			temp_form = form.save(commit = False)
			temp_form.set_password(form.cleaned_data["password"])
			temp_form.save()
			return redirect("/settings/user")
	else:
	#Non-POST mode, show only
		form = UserForm(instance=actual_user)
	return render(request,'users/create_edit_user.html', locals())


