from core.models import Company
from django.conf import settings

def logo_company(request):
    Comanpies = Company.objects.all().count()
    if Comanpies > 0:
        logo = settings.MEDIA_ROOT + Company.objects.latest('id').logo.url
    else:
        logo = settings.STATIC_URL + "media/logo/tk-tiny.png"

    return {'logo': logo}
