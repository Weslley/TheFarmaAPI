from rest_framework import generics

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
