from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, _positive_int


class CustomPageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        try:
            num_pages = self.page.paginator.num_pages
        except:
            num_pages = 0

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_pages', num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class ExtraLargeResultsSetPagination(CustomPageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class LargeResultsSetPagination(CustomPageNumberPagination):
    page_size = 2000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class StandardResultsSetPagination(CustomPageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class SmallResultsSetPagination(CustomPageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000
