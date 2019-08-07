from itertools import groupby

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.models.produto import Produto
from api.models.apresentacao import Apresentacao
from api.models.principio_ativo import PrincipioAtivo

class ListDosagensProdutoView(generics.GenericAPIView):

    def group_by_dict(self, apresentacao):
        """
        Metodo que retorna o dicionario para fazer o group by dos  
        medicamento.
        apresentacao: Apresentacao
        return: Dict
        """

        sufixo_quantidade = apresentacao.sufixo_quantidade.nome if apresentacao.sufixo_quantidade else ''
        embalagem = apresentacao.forma_farmaceutica.nome

        #retorno base
        rs = {
            'dosagem_formatada': apresentacao.dosagem_formatada,
            'embalagem': embalagem,
            'quantidade_embalagem': apresentacao.quantidade,
            'sufixo_quantidade': sufixo_quantidade,
            'embalagem_formatada': apresentacao.embalagem_formatada,
        }

        return rs
        
    def possue_generico_similar(self,produto):
        """
        Verifica se possui generico ou similar
        produto: Str
        return: bool
        """
        principio_ativo = Produto.objects.filter(nome__istartswith=produto)
        if not principio_ativo.count():
            raise ValidationError({'detail':'Produto não encontrado'})
        #recupera o principio ativo
        principio_ativo = principio_ativo.first().principio_ativo
        #ve se tem mais um
        quantidade = Produto.objects.filter(principio_ativo=principio_ativo).distinct('nome').count()
        return True if quantidade  > 1 else False


    def get_queryset(self):
        qs = Produto.objects.filter(nome__iexact=self.request.query_params.get('nome', None))
        if not qs.count():
            raise ValidationError({'detail': 'Produto não encontrado'})
        return qs

    def get(self,request,*args,**kwargs):
        #variavel de retorno
        rs = {
            'generico': self.possue_generico_similar(request.query_params.get('nome', None)),
            'results':[]
        }
        #seleciona todas as apresentacoes do produto
        apresentacoes = Apresentacao.objects.filter(produto__in=self.get_queryset(), comercializado=True)\
            .exclude(forma_farmaceutica=None).order_by('quantidade','embalagem','quantidade')
        
        #agrupa por {dosagem,embalagem,quantidade e sufixo quantidade}
        for k,g in groupby(list(apresentacoes), key=lambda x:x.dosagem_formatada):
            l = []
            for x in g:
                l.append({ 
                    'id': x.id,
                    'embalagem': x.embalagem_formatada,
                    'quantidade_embalagem': x.quantidade,
                    'fabricante': x.fabricante,
                    'imagem': x.imagem_url,
                })

            #prepara a lista de retorno
            #contendo a lista de apresentacoes
            item = { 
                'dosagem_formatada': k,
                'apresentacoes': l 
            }
            
            rs['results'].append(item)

        return Response(rs)
        
