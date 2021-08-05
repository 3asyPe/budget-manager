from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from app import apis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', apis.test_api),
    path('', include('accounts.urls')),
    path('', include('currencies.urls')),
    path('', include('wallets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
