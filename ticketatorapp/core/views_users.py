# User views: list, create, delete
from django.contrib.auth import get_user_model
from core.models import UserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

User = get_user_model()


# List tickets
def list_users(request, state_id=None):
    if request.user.is_superuser:
        user_list = User.objects.all().order_by("-id")
    else:
        user_list = User.objects.filter(id=request.user.id)
    return render(request, 'users/list_users.html', locals())


def manage_user(request, user_id=None):
    # Try to locate the object to use it as an instance and if not, create a new one
    # to use it in a new form.
    # common_data = common_ticket_data()
        if request.user.is_superuser:
            if user_id:
                actual_user = get_object_or_404(User, pk=user_id)
            else:
                actual_user = User()
        else:
            if user_id and int(user_id) == request.user.id:
                actual_user = get_object_or_404(User, pk=user_id)
            else:
                raise Http404
        # POST mode
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES, request=request, instance=actual_user)
            if form.is_valid():
                temp_form = form.save(commit=False)
                #If no modifications were made to password fields...
                if  (not form.cleaned_data["password_first"] and not form.cleaned_data["password_check"]) and form.instance.pk is not None:
                    pass
                else:
                    #Validated by models, once password_check is cleaned, we proceeed updating password...
                    temp_form.set_password(form.cleaned_data["password_check"])
                temp_form.save()
                form.save_m2m()
                return redirect("/settings/user")
        else:
            # Non-POST mode, show only
            form = UserForm(instance=actual_user, request=request)
        return render(request, 'users/create_edit_user.html', locals())


def delete_user(request, user_id=None):
    if request.user.is_superuser:
        if user_id:
            actual_user = get_object_or_404(User, pk=user_id)
            actual_user.delete()
            return redirect("/settings/user")
        else:
            return HttpResponse("User is not found")
