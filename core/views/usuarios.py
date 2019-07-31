# from awesome_mixins.mixins.list import ListMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView

from core.views.mixins import AdminBaseMixin


class PerfilView(DetailView, AdminBaseMixin):
    model = User
    pk_url_kwarg = 'id'


class PerfilUpdate(UpdateView, AdminBaseMixin):
    model = User
    pk_url_kwarg = 'id'
