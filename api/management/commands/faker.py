from django.core.management.base import BaseCommand
from api.models.endereco import Endereco
from api.models.apresentacao import Apresentacao
from api.models.pedido import Pedido
import requests
import datetime
import random
import dateutil
import time
from api.tasks.contas import faturar_pedido

#fake_do_fake = {'id': 1352, 'valor_frete': '0.00', 'status': 0, 'log': {'id': 1358, 'data_criacao': 1548364345128, 'data_atualizacao': 1548364345129, 'remote_ip': '201.131.164.166', 'browser': 'python-requests/2.18.3'}, 'forma_pagamento': 0, 'latitude': -5.0635121, 'longitude': -42.796581, 'delivery':  False, 'troco': '0.00', 'itens': [{'apresentacao': 12298, 'quantidade': 1, 'valor_unitario': '0.00', 'status': 0}, {'apresentacao': 8332, 'quantidade': 4, 'valor_unitario': '0.00', 'status': 0}], 'uf': None}
#fake_do_fake = {'id': 1319, 'valor_frete': '0.00', 'status': 0, 'log': {'id': 1358, 'data_criacao': 1548364345128, 'data_atualizacao': 1548364345129, 'remote_ip': '201.131.164.166', 'browser': 'python-requests/2.18.3'}, 'forma_pagamento': 0, 'latitude': -5.0635121, 'longitude': -42.796581, 'delivery':  False, 'troco': '0.00', 'itens': [{'apresentacao': 126, 'quantidade': 1, 'valor_unitario': '0.00', 'status': 0}], 'uf': None}
fake_do_fake = {'id': 1362, 'valor_frete': '0.00', 'status': 0, 'log': {'id': 1368, 'data_criacao': 1548710920638, 'data_atualizacao': 1548710920639, 'remote_ip': '201.131.164.166', 'browser': 'python-requests/2.18.3'}, 'forma_pagamento': 1, 'latitude': -5.0635121, 'longitude': -42.796581, 'delivery': False, 'troco': '0.00', 'itens': [{'apresentacao': 9644, 'quantidade': 1, 'valor_unitario': '0.00', 'status': 0}], 'uf': None}

class Command(BaseCommand):
    registrar = False
    token = "" #token da farmacia
    token_final = "" #token do usuario final
    mes1 = None #datetime
    mes2 = None #datetime
    mes3 = None #datetime
    quantidade = random.randint(1,5)
    latitude = '-5.0635121'
    longitude = '-42.796581'
    farmacia = {}
    cliente = {}
    meses = 3
    header_cliente = {} #header das requisicoes para o cliente
    header_farmacia = {} #header para as requisicoes da farmacia
    url_base = 'https://api.thefarma.com.br/' #url base do sistema
    #url_base = 'http://localhost:8000/' #url base do sistema
    url_pedido = 'pedidos/' #fazer pedido
    url_login = 'auth/farmacia/login/' #farmacia
    url_login_cliente_final = 'auth/login/' #cliente(app)

    def handle(self, *args, **options):
        self.formata_urls()
        if self.registrar:
            email,senha = self.criar_farmacia()
            rs_login = self.logar(email,senha)
        else:
            rs_login = self.logar('f@f.com','admg2')
            #rs_login = self.logar('x@x.com','teste@1234')
        #recupera token
        if rs_login:
            self.token = rs_login['token']
        else:
            return None
        #logar usuario final
        rs_login_usuario_final = self.login_cliente_final('email@email.com','password')
        if rs_login_usuario_final:
            self.token_final = rs_login_usuario_final['token']
        else:
            print('Falha no login do usuario final')
            return None
        self.gera_mes() # gera os meses que deve ser feito as vendas
        self.monta_headers() #monta os headers
        #recupera o cartao
        #cartao = self.get_cartoes_cliente(self.cliente)
        #cria vendas em todos os dias
        while(self.meses):
            for i in range(1,31):
                try:
                    for j in range(1,random.randint(2,3)):
                        medicamentos_ids = self.get_random_apresentacao_ids() #recupera os ids das apresentacoes
                        pedido = self.fazer_pedido(medicamentos_ids) #faz um pedido
                        #pedido = fake_do_fake
                        if pedido:
                            proposta = self.fazer_proposta(pedido) #faz a proposta
                        else:
                            print('Erro ao fazer pedido!')
                        if proposta:
                            aceita = self.aceita_proposta(pedido)
                        else:
                            print('Erro ao fazer proposta!')
                        if aceita:
                            entrega = self.entrega_pedido(pedido)
                        else:
                            print('Erro ao aceitar!')
                        if entrega:
                            pedido = self.altera_data_pedido(pedido,i,self.meses)
                        else:
                            print('Erro ao entregrar')
                        faturar_pedido(pedido)
                except Exception as err:
                    print('ERROR\n\n')
                    print(str(err))
            self.meses -= 1
            print('\n\n\MESES:{}\n\n'.format(self.meses))
    def login_cliente_final(self,username,password,type=0):
        """
        faz o login do usuario

        username: String
        password: String
        return: Dict
        """
        data = {
            'email':username,
            'password':password,
            'login_type':type,
        }
        r = requests.post(self.url_login_cliente_final,data=data)
        if r.status_code in [200,201]:
            self.cliente = r.json()
            return r.json()
        else:
            print('Login Cliente Final OK')
            return None

    def criar_farmacia(self):
        """
        Cria email e senha para a farmacia
        """
        pass

    def logar(self,email,password):
        """
        Faz o login da farmacia no the farma 
        """
        r = requests.post(self.url_login,data={
            'email':email,
            'password':password
        })
        if r.status_code == 200:
            self.farmacia = r.json()
            print('Login OK')
        else:
            return None
        return r.json()

    
    def gera_mes(self):
        """
        Gera os meses das propostas
        """
        hoje = datetime.datetime.now()
        self.mes1 = datetime.datetime(hoje.year,hoje.month,1)
        self.mes2 = self.mes1 - dateutil.relativedelta.relativedelta(months=1)
        self.mes3 = self.mes2 - dateutil.relativedelta.relativedelta(months=1)
    
    def get_random_apresentacao_ids(self):
        """
        Recupera os id de apresentacoes aleatorias
        return: List<Medicamento>
        """
        rs = []
        ap = Apresentacao.objects.all()[:500]
        for i in range(self.quantidade):
            rs.append(ap[random.randint(1,500)])
            print('Medicamento:' + str(rs[-1].id))
        return rs
    
    def fazer_pedido(self,medicamentos):
        """
        Metodo para criar um pedido  
        medicamento: List<Medicamento>  
        return:Dict
        """
        itens = []
        data = {
            'latitude':self.latitude,
            'longitude':self.longitude,
            'delivery':False,
            'forma_pagamento':1
        }
        headers = {
            'Authorization':'Token {}'.format(self.token_final)
        }
        #povar itens
        for medicamento in medicamentos:
            itens.append({
                'apresentacao':medicamento.id,
                'quantidade':random.randint(1,5)
            })
        #add na requisicao
        data['itens'] = itens
        r = requests.post(self.url_pedido,json=data,headers=headers)
        try:
            print('retorno da criacao:')
            print(r.json())
            time.sleep(1)
            return r.json()
        except Exception as err:
            print(err)
            print('Falha em fazer pedido')
            return None

    def get_endereco(self):
        """
        Return: Int
        """
        return Endereco.objects.values('id').last()['id']
    
    def formata_urls(self):
        """
        Adiciona a url base as urls
        """
        self.url_login = '{}{}'.format(self.url_base,self.url_login)
        self.url_login_cliente_final = '{}{}'.format(self.url_base,self.url_login_cliente_final)
        self.url_pedido = '{}{}'.format(self.url_base,self.url_pedido)
    
    def monta_headers(self):
        """
        Monta os headers das requisicoes
        """
        #cliente(app)
        self.header_cliente = {
            'Authorization':'Token {}'.format(self.token_final)
        }
        #farmacia
        self.header_farmacia = {
            'Authorization':'Token {}'.format(self.token)
        }


    def fazer_proposta(self,pedido):
        """
        Faz a farmacia realizar uma propostas para o pedido  
        pedido_id: Int  
        return: Dict
        """
        url = self.get_url_pedido_proposta(pedido)
        itens_proposta = [] 
        data_proposta = {
            'id':pedido['id']
        }
        pedido = self.get_itens_pedido(pedido,self.header_farmacia)
        
        #monta os pedidos
        for item in pedido['itens_proposta']:
            itens_proposta.append({
                'quantidade':random.randint(1,item['quantidade']),
                'id':item['id'],
                'valor_unitario':"{0:.2f}".format(random.uniform(1, 50)),
                'possui':True,
            })
        #inclui no json
        data_proposta['itens_proposta'] = itens_proposta
        #faz a request
        r = requests.patch(url,json=data_proposta,headers=self.header_farmacia)
        try:
            print('resultado da proposta')
            print(r.json())
            time.sleep(1)
            return r.json()
        except Exception as err:
            print(err)
            return None
        
    def get_itens_pedido(self,pedido,header):
        """
        Recupera os itens pedidos de um pedido  
        pedido: Dict  
        return: Dict  
        """
        url = self.get_url_pedido_proposta(pedido)
        r = requests.get(url,headers=header)
        try:
            print('resultado dos itens pedido')
            print(r.json())
            time.sleep(1)
            return r.json()
        except Exception as err:
            print(str(err))
            return None

    
    def get_url_pedido_proposta(self,pedido):
        """
        Recupera a url da proposta de um pedido  
        pedido: Dict  
        return: String  
        """
        return '{}pedidos/{}/propostas/'.format(self.url_base,pedido['id']) #formata url
    
    def get_url_pedido_checkout(self,pedido):
        """
        Recupera a url da proposta de um pedido  
        pedido: Dict  
        return: String  
        """
        return '{}pedidos/{}/checkout/'.format(self.url_base,pedido['id']) #formata url

    def aceita_proposta(self,pedido,cartao=None):
        """
        Faz o cliente aceitar uma proposta  
        pedido: Dict  
        return: Dict 
        """
        url = self.get_url_pedido_checkout(pedido)
        troco = self.calcula_troco(pedido)
        data = {
            'troco':float('{:.2f}'.format(troco)),
            'farmacia':self.farmacia['farmacia_id'],
            'forma_pagamento':1,
            'numero_parcelas:':1,
        }
        if cartao:
            data.update({
                'forma_pagamento':0,
                'cartao':cartao[0]['id'] 
            })
        print(data)
        print('checkout:')
        #faz requisicao
        r = requests.put(url,headers=self.header_cliente,json=data)
        try:
            print(r.json())
            time.sleep(1)
            return r.json()
        except:
            return None

    
    def calcula_troco(self,pedido):
        """
        Calcula o total da proposta e gera um valor de troco  
        pedido: Dict  
        return: Float  
        """
        url = self.get_url_pedido_proposta(pedido)
        total = 0
        data = self.get_itens_pedido(pedido,self.header_farmacia)

        for item in data['itens_proposta']:
            total += float(item['valor_unitario'])*float(item['quantidade'])
        print('troco:')
        print(total)
        total += random.randint(0,20)
        print(total)
        return total
    
    def entrega_pedido(self,pedido):
        """
        Farmacia informa que o pedido foi entregue  
        pedido: Dict  
        return: Dict  
        """
        url = ' {}pedidos/{}/confirmar_entrega/'.format(self.url_base,pedido['id'])
        r = requests.post(url,headers=self.header_farmacia,json={})
        try:
            print('entrega o pedido:')
            print(r.json())
            time.sleep(1)
            return r.json()
        except Exception as err:
            print(str(err))
            return None
    
    def altera_data_pedido(self,pedido,dias,mes):
        """
        Altera a data e o log da criacao  
        pedido: Dict  
        """
        pedido = Pedido.objects.get(pk=pedido['id'])
        if mes == 3:
            data = self.mes1
            print(data.month)
        elif mes == 2:
            data = self.mes2
            print(data.month)
        elif mes == 1:
            data = self.mes3
            print(data.month)
        print(data)
        try:
            #atualiza a data do pedido
            pedido.data_criacao = datetime.datetime(data.year,data.month,dias)
            pedido.data_atualizacao = datetime.datetime(data.year,data.month,dias)
            pedido.save()
            #atualiza o log
            pedido.log.data_criacao = datetime.datetime(data.year,data.month,dias)
            pedido.log.data_atualizacao = datetime.datetime(data.year,data.month,dias)
            pedido.log.save()
            return pedido
        except Exception as err:
            print('Erro:\n\n')
            print(str(err))
            return pedido
    
    def get_cartoes_cliente(self,cliente):
        """
        Recupera o cartao do cliente
        cliente: Dict
        return: List<Dic>
        """
        url = '{}clientes/{}/cartoes/'.format(self.url_base,cliente['id'])
        try:
            r = requests.get(url,headers=self.header_cliente)
            print(r.json())
            return r.json()
        except Exception as err:
            print(str(err))
            return None