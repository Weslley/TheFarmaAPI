from rest_framework.generics import CreateAPIView


class CreateUpdateMixin(CreateAPIView):
    obj = None

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        return self.create(request, *args, **kwargs)
