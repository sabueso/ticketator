from django.conf import settings


def logo_company(request):

    return {'logo': settings.LOGO_COMPANY}
