from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import LazySettings

settings = LazySettings()

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),


]

#  Add url to serve media elements on development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
