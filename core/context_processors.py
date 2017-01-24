from core.models import Company
from django.conf import settings

def logo_company(request):
    if Company.objects.latest('id'):
        logo = settings.MEDIA_ROOT + Company.objects.latest('id').logo.url
    else:
        logo = settings.STATIC_URL + "media/logo/tk-tiny.png"

    return {'logo': logo}
