# -*- coding: utf-8 -*-

from django.conf.urls import url
from core.views.base import *
from core.views.posts import *
from core.views.usuarios import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    # Post
    url(r'^posts/$', PostList.as_view(), name='post-admin-list'),
    url(r'^posts/adicionar/$', PostCreate.as_view(), name='post-admin-add'),

    # Usuario
    url(r'^perfil/(?P<id>[0-9]+)/$', PerfilView.as_view(), name='perfil-view'),

]
