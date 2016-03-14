#User views: list, create, delete
from django.contrib.auth.models import User
from core.models import UserForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


#List tickets
def list_users(request, state_id=None):
	user_list = User.objects.all().order_by("-id")
	return render(request, 'users/list_users.html', locals())

def manage_user(request, user_id=None):
	#site_vars = utils.site_vars()
	#Common data
	#common_data = common_ticket_data()
	if user_id:
		#Check if existis or raise 404	
		actual_user=get_object_or_404(User,pk=user_id)
	else:
		#If not, assign a new ticket instance to be use as instance of form
		actual_user = User()
	#POST mode
	if request.method == 'POST':
		form = UserForm(request.POST, instance = actual_user)
		if form.is_valid():
			#new_state_form = form.save(commit=False)
			#new_state_form.create_user = request.user
			new_state_form.save()
			return redirect("/users")
	else:
	#Non-POST mode, show only
		form = UserForm(instance=actual_user)
	return render(request,'users/create_edit_user.html', locals())


