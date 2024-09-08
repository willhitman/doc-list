# from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor Directory API",
        default_version='v1',
        description="Doctor Directory API",
        terms_of_service="",
        contact=openapi.Contact(email="giftwt9wt@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
    authentication_classes=[]
)
urlpatterns = ([
                   path('api/v1/accounts/', include('accounts.urls')),
                   path('api/v1/utils/', include('utils.insurances.urls')),
                   path('api/v1/utils/', include('utils.address.urls')),
                   path('api/v1/utils/', include('utils.languages.urls')),
                   path('api/v1/utils/', include('utils.service.urls')),
                   path('api/v1/listings/', include('listings.urls')),
                   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
               static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT))
