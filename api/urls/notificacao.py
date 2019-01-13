from django.conf.urls import url

from api.views.notificacao import NotificacaoList, NotificacaoUpdate, VisualizarNotificacao

urlpatterns = [
    url(r'^$', NotificacaoList.as_view(), name='notificacao-list'),
    url(r'^(?P<pk>[0-9]+)/$', NotificacaoUpdate.as_view(), name='notificacao-update'),
    url(r'^(?P<id>[0-9]+)/visualizar$', VisualizarNotificacao.as_view(), name='notificacao-visualizar'),
]
