# Company views: list, create, delete

from core.models import Rights, RightForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


# List tickets
def list_rights(request):
    if request.user.is_superuser:
        rights_list = Rights.objects.all().order_by('grp_src_id', '-queue_dst')
    else:
        raise Http404
    return render(request, 'rights/list_rights.html', locals())


def manage_right(request, right_id=None):
    if request.user.is_superuser:
        if right_id:
            actual_right = get_object_or_404(Rights, pk=right_id)
        else:
            actual_right = Rights()
        # POST mode
        if request.method == 'POST':
            form = RightForm(request.POST, instance=actual_right)
            if form.is_valid():
                form.save()
                return redirect("/settings/rights")
        else:
            # Non-POST mode, show only
            form = RightForm(instance=actual_right)
        return render(request, 'rights/create_edit_right.html', locals())
    else:
        raise Http404

# some unusefull comment
# another one
