from django.conf.urls import url

from api.views.post import *

urlpatterns = [
    # Post
    url(r'^$', PostExportList.as_view(), name='post-list'),
    url(r'^(?P<id>[0-9]+)/like/$', CurtirView.as_view(), name='post-like'),
    url(r'^likes/$', PostsCurtidosView.as_view(), name='like-list'),
]
