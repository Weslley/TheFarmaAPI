from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token

from core.views.mixins import AdminBaseMixin


class HomeView(TemplateView, AdminBaseMixin):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token, created = Token.objects.get_or_create(user=self.request.user)
        context['token'] = token
        return context
    


def desativa_usuario(request, id, fk_id, model):
    u = User.objects.get(id=id)
    u.is_active = False
    u.save()
    return redirect('{}-admin-view'.format(model), fk_id)
