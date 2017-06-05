# Company views: list, create, delete

from core.models import Company, CompanyForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


# List tickets
def list_companies(request, state_id=None):
    if request.user.is_superuser:
        user_list = Company.objects.all().order_by("-id")
        return render(request, 'companies/list_companies.html', locals())
    else:
        raise Http404


def manage_company(request, company_id=None):
    if request.user.is_superuser:
        # Try to locate the object to use it as an instance and if not, create
        # new one to use it in a new form.
        # common_data = common_ticket_data()
        if company_id:
            actual_company = get_object_or_404(Company, pk=company_id)
        else:
            actual_company = Company()
        # POST mode
        if request.method == 'POST':
            form = CompanyForm(
                request.POST, request.FILES, instance=actual_company)
            if form.is_valid():
                form.save()
                return redirect("/settings/companies")
        else:
            # Non-POST mode, show only
            form = CompanyForm(instance=actual_company)
        return render(request, 'companies/create_edit_company.html', locals())
    else:
        raise Http404
