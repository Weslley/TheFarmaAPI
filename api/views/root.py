from django.contrib.auth.models import User
from django.http.response import Http404
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_docs.api_docs import ApiDocumentation
from rest_framework_docs.settings import DRFSettings

from api.urls import urls
from core.views.mixins import AdminBaseMixin


class HomeApiView(TemplateView):
    template_name = 'indexapi.html'


class HomeApiViewOld(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    urls_names = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        context = {}
        for url in self.urls_names:
            if url != 'produto-list' and url != 'bairro-list':
                context[url[:-5]] = reverse(url, request=request, format=format)
        return Response(context)

    def show_urls(self):
        self.urls_names = []
        self.load_urls(urls.urlpatterns)

    def dispatch(self, request, *args, **kwargs):
        self.show_urls()
        return super(HomeApiView, self).dispatch(request, *args, **kwargs)

    def load_urls(self, urllist):

        for entry in urllist:
            if hasattr(entry, 'name'):
                if entry.name and entry.name.endswith('-list'):
                    self.urls_names.append(entry.name)
            if hasattr(entry, 'url_patterns'):
                self.load_urls(entry.url_patterns)


class DRFDocsView(TemplateView, AdminBaseMixin):

    template_name = "rest_framework_docs/home.html"

    def get_context_data(self, **kwargs):
        settings = DRFSettings().settings
        if settings["HIDE_DOCS"]:
            raise Http404("Django Rest Framework Docs are hidden. Check your settings.")

        context = super(DRFDocsView, self).get_context_data(**kwargs)
        docs = ApiDocumentation()
        endpoints = docs.get_endpoints()

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context
