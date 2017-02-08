from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response
from collections import OrderedDict


class CustomPageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size


class ExtraLargeResultsSetPagination(CustomPageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class LargeResultsSetPagination(CustomPageNumberPagination):
    page_size = 5000
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class StandardResultsSetPagination(CustomPageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class SmallResultsSetPagination(CustomPageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000
