# -*- coding: utf-8 -*-

from django.conf.urls import url
from core.views.base import *
from core.views.posts import PostList

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    # Post
    url(r'^posts/$', PostList.as_view(), name='post-admin-list'),

]
