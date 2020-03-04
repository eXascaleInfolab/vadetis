"""vadetis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found
from vadetisweb.urls import apipatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Vadetis API",
        default_version='v1',
        description="API for Vadetis",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lisaexascale@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # todo only for authenticated user
    patterns=apipatterns
)

urlpatterns = [
    path('', include('vadetisweb.urls', namespace='vadetisweb')),
    path('accounts/password/set/', page_not_found, {'exception': Exception()}),
    path('accounts/password/change/', page_not_found, {'exception': Exception()}),
    path('accounts/social/connections/', page_not_found, {'exception': Exception()}),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),

    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
