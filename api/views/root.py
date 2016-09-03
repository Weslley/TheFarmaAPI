from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from api import urls


class HomeApiView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        l = urls.urlpatterns
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)