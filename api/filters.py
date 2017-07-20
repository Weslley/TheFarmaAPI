import django_filters
from rest_framework.filters import BaseFilterBackend

from api.models.bairro import Bairro
from api.models.cidade import Cidade
from api.models.produto import Produto
from api.models.apresentacao import Apresentacao


class MedicamentoFilter(django_filters.rest_framework.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Produto
        fields = ['nome', ]


class ProdutoFilter(django_filters.rest_framework.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')
    secao = django_filters.CharFilter(name="secao", lookup_expr='nome__istartswith')
    subsecao = django_filters.CharFilter(name="subsecao", lookup_expr='nome__istartswith')

    class Meta:
        model = Produto
        fields = ['nome', 'secao', 'subsecao']


class OrderingFilter(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('order', '')
        ordering = ordering.split(',')
        order_list = []
        for order in ordering:
            if order in view.ordering_fields:
                order_list.append(order)

        if order_list:
            return queryset.order_by(*order_list)
        else:
            return queryset.order_by(*[order for order in view.ordering])


class CidadeFilter(django_filters.rest_framework.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Cidade
        fields = ['nome', ]


class BairroFilter(django_filters.rest_framework.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Bairro
        fields = ['nome', ]


class ApresentacaoFilter(django_filters.rest_framework.FilterSet):
    nome = django_filters.CharFilter(name="produto__nome", lookup_expr='istartswith')
    secao = django_filters.CharFilter(name="produto__secao", lookup_expr='nome__istartswith')
    subsecao = django_filters.CharFilter(name="produto__subsecao", lookup_expr='nome__istartswith')

    class Meta:
        model = Apresentacao
        fields = ['nome', 'secao', 'subsecao']
