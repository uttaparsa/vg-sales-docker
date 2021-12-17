"""config URL Configuration

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
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analysis/', include('analysis.urls')),
]
if settings.DEBUG:
    urlpatterns.append(path('api/schema/', SpectacularAPIView.as_view(), name='schema'),)
    urlpatterns.append(path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),)