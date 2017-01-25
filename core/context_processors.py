from core.models import Company
from django.contrib.staticfiles.templatetags.staticfiles import static


def logo_company(request):

    try:
        company = Company.objects.latest('id')
        if company.logo:
            logo = company.logo.url
    except Company.DoesNotExist:
        # Resolve static url if no company creted
        logo = static("images/logo/tk-tiny.png")

    return {'logo': logo}
