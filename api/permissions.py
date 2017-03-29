from rest_framework import permissions
from rest_framework.compat import is_authenticated


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
