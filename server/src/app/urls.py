from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from app import apis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', apis.test_api),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
