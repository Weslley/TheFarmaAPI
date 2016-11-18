from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView


class IsAuthenticatedMixin(APIView):
    """
    Mixin para views que a autenticação é obrigatória
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)


class CustomJSONAPIView(object):
    """
    Mixin para APIView de dados básicos
    """
    serializer_class = None

    def get_data(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            return serializer.create(serializer.validated_data)
        except:
            return None
