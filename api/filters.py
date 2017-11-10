import django_filters
import six
from django.db.models.query_utils import Q
from django_filters.constants import STRICTNESS
from rest_framework.filters import BaseFilterBackend

from api.models.apresentacao import Apresentacao
from api.models.bairro import Bairro
from api.models.cidade import Cidade
from api.models.enums.status_item_proposta import StatusItemProposta
from api.models.enums.status_pedido import StatusPedido
from api.models.pedido import Pedido
from api.models.produto import Produto

from django import forms


class PropostaFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(name="status")

    class Meta:
        model = Pedido
        fields = ['status']

    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            if not self.is_bound:
                self._qs = self.queryset.all()
                return self._qs

            if not self.form.is_valid():
                if self.strict == STRICTNESS.RAISE_VALIDATION_ERROR:
                    raise forms.ValidationError(self.form.errors)
                elif self.strict == STRICTNESS.RETURN_NO_RESULTS:
                    self._qs = self.queryset.none()
                    return self._qs
                    # else STRICTNESS.IGNORE...  ignoring

            # start with all the results and filter from there
            qs = self.queryset.all()
            for name, filter_ in six.iteritems(self.filters):
                if name == 'status':
                    qs = self.filter_status(filter_, qs)
                else:
                    value = self.form.cleaned_data.get(name)

                    if value is not None:  # valid & clean data
                        qs = filter_.filter(qs, value)

            self._qs = qs

        return self._qs

    def filter_status(self, filter, queryset):
        """
        0 ==> Aberto
        2 ==> Aguardando envio da farmácia
        3 ==> Aguardando retirada do cliente
        4 ==> Enviado
        5 ==> Entregue
        6 ==> Cancelado pela farmácia
        7 ==> Cancelado pelo cliente
        10 ==> Negado
        9 ==> Tempo excedido
        :param filter: 
        :param queryset: 
        :return: 
        """
        value = self.form.cleaned_data.get('status')

        if value is None:
            return queryset

        farmacia = self.request.user.representante_farmacia.farmacia

        if value == 0:
            queryset = filter.filter(queryset, value)
            queryset = queryset.filter(
                itens_proposta__status=StatusItemProposta.ABERTO.value,
                itens_proposta__farmacia=farmacia
            )

        elif value == 2:
            queryset = filter.filter(queryset, value)
            queryset = queryset.filter(farmacia=farmacia)

        elif value == 3:
            queryset = filter.filter(queryset, value)
            queryset = queryset.filter(farmacia=farmacia)

        elif value == 4:
            queryset = filter.filter(queryset, value)
            queryset = queryset.filter(farmacia=farmacia)

        elif value == 5:
            queryset = filter.filter(queryset, value)
            queryset = queryset.filter(farmacia=farmacia)

        elif value == 6:
            queryset = queryset.filter(
                Q(itens_proposta__status=StatusItemProposta.CANCELADO.value, itens_proposta__farmacia=farmacia) |
                Q(farmacia=farmacia, status=value)
            )

        elif value == 7:
            queryset = filter.filter(queryset, value)

        elif value == 9:
            queryset = queryset.filter(
                itens_proposta__status=StatusItemProposta.ABERTO.value,
                itens_proposta__farmacia=farmacia,
                status=value,
                farmacia__isnull=True
            )

        elif value == 10:
            queryset = queryset.filter(
                Q(status=StatusPedido.AGUARDANDO_ENVIO_FARMACIA.value) |
                Q(status=StatusPedido.AGUARDANDO_RETIRADA_CLIENTE.value) |
                Q(status=StatusPedido.ENVIADO.value) |
                Q(status=StatusPedido.ENTREGUE.value) |
                Q(status=StatusPedido.CANCELADO_PELA_FARMACIA.value) |
                Q(status=StatusPedido.TIMEOUT),
                itens_proposta__status=StatusItemProposta.ENVIADO.value,
                itens_proposta__farmacia=farmacia,
            ).exclude(farmacia=farmacia)

        queryset = queryset.distinct()

        return queryset


class MedicamentoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Produto
        fields = ['nome', ]


class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')
    secao = django_filters.CharFilter(name="secao", lookup_expr='nome__istartswith')
    subsecao = django_filters.CharFilter(name="subsecao", lookup_expr='nome__istartswith')
    codigo_barras = django_filters.CharFilter(name="subsecao", lookup_expr='apresentacoes__codigo_barras')

    class Meta:
        model = Produto
        fields = ['nome', 'secao', 'subsecao', 'codigo_barras']


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


class CidadeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Cidade
        fields = ['nome', ]


class BairroFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(name="nome", lookup_expr='istartswith')

    class Meta:
        model = Bairro
        fields = ['nome', ]


class ApresentacaoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(name="produto__nome", lookup_expr='istartswith')
    secao = django_filters.CharFilter(name="produto__secao", lookup_expr='nome__istartswith')
    subsecao = django_filters.CharFilter(name="produto__subsecao", lookup_expr='nome__istartswith')

    class Meta:
        model = Apresentacao
        fields = ['nome', 'secao', 'subsecao']
