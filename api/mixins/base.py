from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView


class IsAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)