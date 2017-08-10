from django.conf.urls import url

from api.views.post import *


urlpatterns = [
    # Post
    url(r'^posts/$', PostExportList.as_view(), name='post-list'),
    url(r'^posts/(?P<id>[0-9]+)/like/$', CurtirView.as_view(), name='post-like'),
    url(r'^posts/likes/$', PostsCurtidosView.as_view(), name='like-list'),
]
