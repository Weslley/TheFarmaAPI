from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.base import IsAuthenticatedMixin
from api.models.curtida import Curtida
from api.models.post import Post
from api.pagination import StandardResultsSetPagination
from api.serializers.post import PostExportSerializer


class PostExportList(generics.ListAPIView):
    """
    Listagem dos posts para exportar
    """
    queryset = Post.objects.all()
    serializer_class = PostExportSerializer
    pagination_class = StandardResultsSetPagination


class CurtirView(IsAuthenticatedMixin):
    """
    Class based view para curtida
    """

    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        curtida, create = Curtida.objects.get_or_create(post=post, usuario=request.user)

        if not create:
            curtida.delete()

        return Response({'curtida': create}, status=status.HTTP_200_OK)
