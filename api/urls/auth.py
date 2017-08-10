from django.conf.urls import url

from api.views.autenticacao import Logout, LoginFacebook, TesteLogin, LoginFarmacia, Login, LoginDefault, CreateUser


urlpatterns = [
    # Login token
    url(r'^login/$', TesteLogin.as_view(), name='login'),
    url(r'^login_facebook/$', LoginFacebook.as_view(), name='login-facebook'),
    url(r'^login/cliente/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^auth/logout/$', Logout.as_view(), name='logout'),
    url(r'^auth/users/$', CreateUser.as_view(), name='create-user'),
    url(r'^auth/login/$', LoginDefault.as_view(), name='login-user'),
    url(r'^auth/farmacia/login/$', LoginFarmacia.as_view(), name='login-farmacia'),
]
