from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from api.models.produto import Produto
from api.models.apresentacao import Apresentacao
from itertools import groupby
from apiv2.utils.formartar import gerar_nome_dosagem
from api.models.principio_ativo import PrincipioAtivo
from api.models.apresentacao import EXECOES
from api.utils.formats import formata_numero_apresentaca

class ListDosagensProdutoView(generics.GenericAPIView):

    def group_by_dict(self,apresentacao):
        """
        Metodo que retorna o dicionario para fazer o group by dos  
        medicamento.
        apresentacao: Apresentacao
        return: Dict
        """
        sufixo_quantidade = apresentacao.sufixo_quantidade.nome if apresentacao.sufixo_quantidade else ''
        embalagem = apresentacao.forma_farmaceutica.nome
        #formata o nome da embalagem
        embalagem_formatada = self.gerar_nome_embalagem(
            embalagem,
            apresentacao.quantidade,
            sufixo_quantidade
        )
        #retorno base
        rs = {
            'dosagem_formatada':gerar_nome_dosagem(apresentacao),
            'embalagem_formatada':embalagem_formatada,
            'embalagem':embalagem,
            'quantidade_embalagem':apresentacao.quantidade,
            'sufixo_quantidade': sufixo_quantidade,
            'dosagens':[]
        }
        #os campos a baixo sao opcionais
        if apresentacao.dosagem:
            rs['dosagens'].append({
                'dosagem':apresentacao.dosagem,
                'sufixo_dosagem':apresentacao.sufixo_dosagem.nome,
                'i':1
            })
        if apresentacao.segunda_dosagem:
            rs['dosagens'].append({
                'dosagem':apresentacao.segunda_dosagem,
                'sufixo_dosagem':apresentacao.sufixo_segunda_dosagem.nome,
                'i':2
            })
        if apresentacao.terceira_dosagem:
            rs['dosagens'].append({
                'dosagem':apresentacao.terceira_dosagem,
                'sufixo_dosagem':apresentacao.sufixo_terceira_dosagem.nome,
                'i':3
            })
        if apresentacao.quarta_dosagem:
            rs['dosagens'].append({
                'dosagem':apresentacao.quarta_dosagem,
                'sufixo_dosagem':apresentacao.sufixo_quarta_dosagem.nome,
                'i':4
            })
        return rs
        

    def gerar_nome_embalagem(self,embalagem,quantidade,sufixo_quantidade):
        """
        Gera o nome da embalagem
        apresentacao: Apresentacao
        return: str
        """
        #formata a quantidade
        quantidade = formata_numero_apresentaca(quantidade)
        #verifica se esta nas execoes de formatacao
        if embalagem in EXECOES:
            nome = '{} {}'.format(quantidade,embalagem)
        else:
            nome = '{} com {}{}'.format(embalagem,quantidade,sufixo_quantidade)
        return nome
    
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
            .exclude(forma_farmaceutica=None).order_by('quantidade','embalagem','quantidade')
        #agrupa por {dosagem,embalagem,quantidade e sufixo quantidade}
        for k,g in groupby(list(apresentacoes), key=lambda x:self.group_by_dict(x)):
            #prepara a lista de retorno
            #contendo a lista de apresentacoes
            item = {
                'apresentacacoes':[x.id for x in g],
            }
            #atualiza com o resto das keys
            item.update(**k)
            rs['results'].append(item)
        return Response(rs)
        
