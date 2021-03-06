"""covid_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title = "COVID-19 API",
      default_version = 'v1',
      description = "A Web API for getting consice and compiled imformation about Covid-19 cases and vaccinations in India.",
      contact = openapi.Contact(email="peter31617@gmail.com"),
      license = openapi.License(name="Open Source License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/rest-auth/',include('rest_auth.urls')),
    path('api/v1/',include('api.urls')),
    path('test/',include('scheduler.urls')),
    path('doc/', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
]
