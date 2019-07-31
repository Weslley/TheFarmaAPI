from rest_framework import permissions
from rest_framework.compat import is_authenticated

from api.models.cliente import Cliente
from api.models.representante_legal import RepresentanteLegal


class IsAuthenticatedInGetPut(permissions.BasePermission):
    """
    Permissão para só poder fazer put e get se estiver authenticado
    """

    def has_permission(self, request, view):

        if request.method in list(permissions.SAFE_METHODS) + ['PUT', 'PATCH']:
            return request.user and is_authenticated(request.user)

        if request.method == 'POST':
            return True

    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user


class IsOwnerClienteEndereco(permissions.BasePermission):
    """
    Permissão para o endereço do cliente
    """

    def has_object_permission(self, request, view, obj):
        try:
            return obj.clienteendereco._cliente.usuario == request.user
        except Exception as err:
            print(err)
            return False


class IsOwnerClienteCartao(permissions.BasePermission):
    """
    Permissão para o cartão do cliente
    """

    def has_object_permission(self, request, view, obj):
        try:
            return obj.cliente.usuario == request.user
        except Exception as err:
            print(err)
            return False


class IsOnlyCliente(permissions.BasePermission):
    """
    Permissão para só ppermitir acesso de usuario que é cliente
    """

    def has_permission(self, request, view):

        if hasattr(request.user, 'cliente') and request.user.cliente:
            if 'id_cliente' in view.kwargs:
                try:
                    cliente = Cliente.objects.get(id=view.kwargs['id_cliente'])
                    return request.user.cliente == cliente
                except Cliente.DoesNotExist:
                    return False

            return True

        else:
            return False

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'cliente') and request.user.cliente:
            if type(obj) == Cliente:
                return obj == request.user.cliente

            if hasattr(obj, 'cliente') and obj.cliente:
                return obj.cliente == request.user.cliente

            return True

        return False


class IsOnlyRepresentante(permissions.BasePermission):
    """
    Permissão para só ppermitir acesso de usuario que é cliente
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'representante_farmacia') and request.user.representante_farmacia

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'representante_farmacia') and request.user.representante_farmacia:
            if type(obj) == RepresentanteLegal and obj == request.user.representante_farmacia:
                return True
            if hasattr(obj, 'representante_farmacia') and obj.representante_farmacia \
                    and obj.representante_farmacia == request.user.representante_farmacia:
                return True
            return True

        return False

