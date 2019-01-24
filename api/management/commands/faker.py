from django.core.management.base import BaseCommand
from api.models.endereco import Endereco
from api.models.apresentacao import Apresentacao
import requests
import datetime
import random
import dateutil

fake_do_fake = {'id': 1352, 'valor_frete': '0.00', 'status': 0, 'log': {'id': 1358, 'data_criacao': 1548364345128, 'data_atualizacao': 1548364345129, 'remote_ip': '201.131.164.166', 'browser': 'python-requests/2.18.3'}, 'forma_pagamento': 0, 'latitude': -5.0635121, 'longitude': -42.796581, 'delivery':  False, 'troco': '0.00', 'itens': [{'apresentacao': 12298, 'quantidade': 1, 'valor_unitario': '0.00', 'status': 0}, {'apresentacao': 8332, 'quantidade': 4, 'valor_unitario': '0.00', 'status': 0}], 'uf': None}
#fake_do_fake = {'id': 1319, 'valor_frete': '0.00', 'status': 0, 'log': {'id': 1358, 'data_criacao': 1548364345128, 'data_atualizacao': 1548364345129, 'remote_ip': '201.131.164.166', 'browser': 'python-requests/2.18.3'}, 'forma_pagamento': 0, 'latitude': -5.0635121, 'longitude': -42.796581, 'delivery':  False, 'troco': '0.00', 'itens': [{'apresentacao': 126, 'quantidade': 1, 'valor_unitario': '0.00', 'status': 0}], 'uf': None}

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
    header_cliente = {} #header das requisicoes para o cliente
    header_farmacia = {} #header para as requisicoes da farmacia
    #url_base = 'https://api.thefarma.com.br/' #url base do sistema
    url_base = 'http://localhost:8000/' #url base do sistema
    url_pedido = 'pedidos/' #fazer pedido
    url_login = 'auth/farmacia/login/' #farmacia
    url_login_cliente_final = 'auth/login/' #cliente(app)

    def handle(self, *args, **options):
        self.formata_urls()
        if self.registrar:
            email,senha = self.criar_farmacia()
            rs_login = self.logar(email,senha)
        else:
            rs_login = self.logar('x@x.com','teste@1234')
        #recupera token
        if rs_login:
            self.token = rs_login['token']
        else:
            return None    
        #logar usuario final
        rs_login_usuario_final = self.login_cliente_final('lucasresone@gmail.com','poupou123')
        if rs_login_usuario_final:
            self.token_final = rs_login_usuario_final['token']
        else:
            print('Falha no login do usuario final')
            return None
        self.gera_mes() # gera os meses que deve ser feito as vendas
        self.monta_headers() #monta os headers
        medicamentos_ids = self.get_random_apresentacao_ids() #recupera os ids das apresentacoes
        #pedido = self.fazer_pedido(medicamentos_ids) #faz um pedido
        pedido = fake_do_fake
        if pedido:
            proposta = self.fazer_proposta(pedido) #faz a proposta
        else:
            print('Erro ao fazer pedido!')
    
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
        Faz o login no the farma
        """
        r = requests.post(self.url_login,data={
            'email':email,
            'password':password
        })
        if r.status_code == 200:
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
        ap = Apresentacao.objects.all()[:100]
        for i in range(self.quantidade):
            rs.append(ap[random.randint(1,100)])
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
            'forma_pagamento':0
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
        print(data)
        r = requests.post(self.url_pedido,json=data,headers=headers)
        try:
            return r.json()
        except:
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
        url = self.get_url_pedido_proposta()
        itens_proposta = [] 
        data_proposta = {
            'id':pedido['id']
        }
        
        #monta os pedidos
        for item in pedido['itens']:
            itens_proposta.append({
                'quantidade':random.randint(1,item['quantidade']),
                'id':item['apresentacao'],
                'valor_unitario':"{0:.2f}".format(random.uniform(1, 50)),
                'possui':True,
            })
        #inclui no json
        data_proposta['itens_proposta'] = itens_proposta
        print(data_proposta)
        #faz a request
        r = requests.patch(url,json=data_proposta,headers=self.header_farmacia)
        print(r.status_code,r.json())
        try:
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
        url = self.get_url_pedido_proposta()
        r = requests.get(url,headers=header)
        try:
            print(r.json())
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

