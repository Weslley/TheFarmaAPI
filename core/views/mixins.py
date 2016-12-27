from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin, View


class AdminBaseMixin(ContextMixin, View):
    """
    Mixin para o admin
    """
    required_permissions = ()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.required_permissions):
            raise PermissionDenied()
        return super(AdminBaseMixin, self).dispatch(request, *args, **kwargs)
