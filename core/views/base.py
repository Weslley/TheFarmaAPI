from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.views.mixins import AdminBaseMixin


class HomeView(TemplateView, AdminBaseMixin):
    template_name = 'index.html'


def desativa_usuario(request, id, fk_id, model):
    u = User.objects.get(id=id)
    u.is_active = False
    u.save()
    return redirect('{}-admin-view'.format(model), fk_id)
