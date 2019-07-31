from django.conf.urls import url

from api.views.conta import ContaList, ContaRetrieve 


urlpatterns = [
    url(r'^$', ContaList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ContaRetrieve.as_view())
]
