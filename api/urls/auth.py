from django.conf.urls import url

from api.views.autenticacao import (CreateUser, LoginCliente, LoginFarmacia,
                                    Logout, EnviarCodigoSmsView)

urlpatterns = [
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^users/$', CreateUser.as_view(), name='create-user'),
    url(r'^login/$', LoginCliente.as_view(), name='login-user'),
    url(r'^enviar_sms/$', EnviarCodigoSmsView.as_view(), name='enviar-sms-user'),
    url(r'^farmacia/login/$', LoginFarmacia.as_view(), name='login-farmacia'),
]
