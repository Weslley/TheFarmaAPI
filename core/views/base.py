from django.views.generic import TemplateView
from core.views.mixins import AdminBaseMixin


class HomeView(TemplateView, AdminBaseMixin):
    template_name = 'index.html'
