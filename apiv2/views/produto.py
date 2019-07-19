from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from api.models.produto import Produto
from api.models.apresentacao import Apresentacao
from itertools import groupby
from apiv2.utils.formartar import gerar_nome_dosagem
from api.models.principio_ativo import PrincipioAtivo

class ListDosagensProdutoView(generics.GenericAPIView):
    
    def possui_generico_similar(self,produto):
        """
        Verifica se possui generico ou similar
        produto: Str
        return: bool
        """
        principio_ativo = Produto.objects.filter(nome__istartswith=produto)\
            .first().principio_ativo
        quantidade = Produto.objects.filter(principio_ativo=principio_ativo)\
            .distinct('nome').count()
        return True if quantidade  > 1 else False


    def get_queryset(self):
        qs = Produto.objects.filter(nome__iexact=self.kwargs.get('nome',None))
        if not qs.count():
            raise ValidationError({'detail':'Produto nao existe'})
        return qs

    def get(self,request,*args,**kwargs):
        #variavel de retorno
        rs = {
            'generico': self.possui_generico_similar(self.kwargs['nome']),
            'results':[]
        }
        #seleciona todas as apresentacoes do produto
        apresentacoes = Apresentacao.objects.filter(produto__in=self.get_queryset())\
            .exclude(forma_farmaceutica=None)
        #agrupa por {dosagem,embalagem}
        for k,g in groupby(list(apresentacoes), key=lambda x:{'dosagem':gerar_nome_dosagem(x),'embalagem':x.forma_farmaceutica.nome}):
            #prepara a lista de retorno
            #contendo a lista de apresentacoes
            rs['results'].append({
                'apresentacacoes':[x.id for x in g],
                'dosagem':k['dosagem'],
                'embalagem':k['embalagem'],
            })
        return Response(rs)
        
