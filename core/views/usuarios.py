# from awesome_mixins.mixins.list import ListMixin
from core.views.mixins import AdminBaseMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView


class PerfilView(DetailView, AdminBaseMixin):
    model = User
    pk_url_kwarg = 'id'
