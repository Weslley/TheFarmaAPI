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
import django.contrib.auth.views as auth_views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import urls as drf_urls
from rest_framework_docs import urls as rest_framework_docs_urls

from api.urls import urls as api_urls
from api.views.root import DRFDocsView
from core import urls as core_urls

urlpatterns = [
    url(r'^', include(api_urls)),
    url(r'^admin/login/', auth_views.login, name='login'),
    url(r'^admin/logout/', auth_views.logout_then_login, {'login_url': '/admin/login'}, name='logout'),
    url(r'^docs/$', DRFDocsView.as_view(), name='drfdocs'),
    url(r'^lucas-admin/', admin.site.urls),
    url(r'^admin/', include(core_urls)),
    url(r'^api-auth/', include(drf_urls, namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
