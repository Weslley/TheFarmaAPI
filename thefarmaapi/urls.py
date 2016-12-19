"""thefarmaapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from rest_framework import urls as drf_urls
from django.conf.urls import url, include
from django.contrib import admin
from api import urls as api_urls
from core import  urls as core_urls
from rest_framework_docs import urls as rest_framework_docs_urls
from django.conf import settings

urlpatterns = [
    url(r'^a/', include(api_urls)),
    url(r'^a/docs/', include(rest_framework_docs_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^admin2/', include(core_urls)),
    url(r'^api-auth/', include(drf_urls, namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
