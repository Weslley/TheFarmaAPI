import requests
from decouple import config
from api.models.notificacao import NotificacoesTemplate, Notificacao, TipoNotificacaoTemplate
from api.models.enums import FormaPagamento

'''
def analisa_pedido_notificacao(temp_notif, pedido):
    """
    Analisa o tipo de pedido e customiza a mensagem
    temp_notif: <NotificacaoTemplate object>
    pedido: <Pedido object>
    """
    if(not pedido.delivery):
        if(pedido.forma_pagamento == FormaPagamento.DINHEIRO):

        elif(pedido.forma_pagamento == FormaPagamento.CARTAO):
'''

def enviar_notif(fcm_token,tipo,cliente_id,pedido=None,extra_data=None):
    """
    Envia uma notificação para um fcm_token  
    fcm_token: String  
    tipo: Int
    pedido: Pedido
    extra_data: Dict 
    return: Dict
    """

    #template da notificacao
    template_notif = NotificacoesTemplate.objects.get(tipo=tipo)


    #header da requisicao pro fire base
    headers = {
        'Authorization': 'Key={}'.format(config('FIREBASE_CHAVE_SERVIDOR')),
        'Content-Type':'application/json'
    }
    #corpo
    body = get_body_requisicao(fcm_token,template_notif,pedido=pedido,extra=extra_data)

    try:
        #cria uma notificacao para o usuario
        data_notificacao = {
            'tipo':0,
            'titulo': template_notif.titulo if template_notif.titulo else None,
            'mensagem': template_notif.menssagem,
            'mensagem_extra': template_notif.mensagem_extra,
            'visualizada':False,
            'cliente_id':cliente_id,
            'pedido':pedido,
        }
        #salva
        notif = Notificacao.objects.create(**data_notificacao)
        #add o id da notificacao no extra_data
        body['data']['data'].update({'notificacao_id':notif.id})
        print(body)
        #envia para o firebase
        r = requests.post('https://fcm.googleapis.com/fcm/send',headers=headers,json=body)
        response_json = r.json()

        if response_json['sucess'] == 1:
            return {'status':True,'messagem':'success','extra_data':response_json}
    except Exception as e:
        print(str(e))
        return {'status':False,'error':str(e)}

def get_body_requisicao(fcm_token,template_notif,pedido=None,extra=None):
    """
    monta o corpo para a requisicao pro push notification
    fcm_token: String
    template_notif: TemplateNotificacao
    pedido: Pedido
    extra: Dict
    return: Dict
    """
    body = {
        'to':fcm_token,
        'collapse_key':'type_a',
        'notification':{
            'title':template_notif.titulo,
            'body':template_notif.menssagem,
            'extra':template_notif.mensagem_extra
        },
        'data':{
            'body':template_notif.titulo,
            'title':template_notif.menssagem,
            'extra':template_notif.mensagem_extra,
            'screen':template_notif.tela,
            'data':extra
        }
    }
    #caso tenha pedido formata para sair o id do pedido
    if pedido:
        body['notification']['body'] = body['notification']['body'].format(pedido.id)
        body['data']['body'] = body['data']['body'].format(pedido.id)
    return body
