# -*- coding: utf-8 -*-

from django.conf.urls import url

from core.views.posts import PostList

urlpatterns = [
    # Post
    url(r'^posts/$', PostList.as_view(), name='post-admin-list'),

]
