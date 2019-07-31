from rest_framework import exceptions
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)


class CreateUpdateMixin(CreateAPIView):
    obj = None

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        return self.create(request, *args, **kwargs)


class ClienteQuerysetOnly(GenericAPIView):
    """
    Mixin para filtrar elementos de acordo com o cliente da requisição
    """

    def get_queryset(self):
        ModelClass = self.serializer_class.Meta.model
        _filter = {'cliente__usuario': self.request.user}
        queryset = ModelClass.objects.filter(**_filter)
        return queryset


class RetrieveUpdateDestroyAPIViewNoPatch(RetrieveUpdateDestroyAPIView):
    """
    Mixin para desabilitar o metodo patch da generic view
    """

    def patch(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)


class UpdateAPIViewNoPatch(UpdateAPIView):
    """
    Mixin para desabilitar o metodo patch da generic view
    """

    def patch(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)
