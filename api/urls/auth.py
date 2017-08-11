from django.conf.urls import url

from api.views.autenticacao import (CreateUser, LoginDefault, LoginFarmacia,
                                    Logout)

urlpatterns = [
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^users/$', CreateUser.as_view(), name='create-user'),
    url(r'^login/$', LoginDefault.as_view(), name='login-user'),
    url(r'^farmacia/login/$', LoginFarmacia.as_view(), name='login-farmacia'),
]
