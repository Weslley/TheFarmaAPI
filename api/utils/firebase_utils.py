import requests
from decouple import config
from api.models.notificacao import NotificacoesTemplate, Notificacao, TipoNotificacaoTemplate

def enviar_notif(fcm_token,tipo,cliente_id,extra_data=None):
    """
    Envia uma notificação para um fcm_token  
    fcm_token: String  
    title: String 
    body: String  
    """

    #template da notificacao
    template_notif = NotificacoesTemplate.objects.get(tipo=tipo)

    #header da requisicao pro fire base
    headers = {
        'Authorization': 'Key={}'.format(config('FIREBASE_CHAVE_SERVIDOR')),
        'Content-Type':'application/json'
    }
    #corpo
    body = {
        'to':fcm_token,
        'collapse_key':'type_a',
        'notification':{
            'title':template_notif.titulo,
            'body':template_notif.mensagem
        },
        'data':{
            'body':template_notif.titulo,
            'title':template_notif.mensagem,
            'screen':template_notif.tela,
        }
    }

    try:
        #envia para o firebase
        r = requests.post('https://fcm.googleapis.com/fcm/send',headers=headers,json=body)
        response_json = r.json()
        print(response_json['sucess'])
        #cria uma notificacao para o usuario
        Notificacao.objects.create({
            'tipo':0,
            'titulo': template_notif.titulo if template_notif.titulo else template_notif.menssagem,
            'mensagem': template_notif.menssagem,
            'visualizada':False,
            'cliente_id':cliente_id
        })
        if response_json['sucess'] == 1:
            return {'status':True,'messagem':'success','extra_data':response_json}
    except Exception as e:
        print(str(e))
        return {'status':False,'extra_data':str(e)}