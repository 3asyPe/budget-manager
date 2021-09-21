from accounts import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_swagger.views import get_swagger_view

from app import apis


schema_view = get_swagger_view(title='Swagger')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', apis.test_api),
    path('', include('accounts.urls')),
    path('', include('currencies.urls')),
    path('', include('wallets.urls')),
    path('', schema_view),
    path('accounts/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
