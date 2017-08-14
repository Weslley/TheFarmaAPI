from django.contrib.auth.models import User
from rest_framework import schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from api.urls import urls


class HomeApiView(APIView):
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


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='API Docs', patterns=urls.urlpatterns, url='/')
    return Response(generator.get_schema())
