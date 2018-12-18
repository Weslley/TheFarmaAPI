import requests
from decouple import config

def enviar_notif(fcm_token,title,body,extra_data=None):
    """
    Envia uma notificação para um fcm_token  
    fcm_token: String  
    title: String  
    body: String  
    """

    headers = {
        'Authorization': 'Key={}'.format(config('FIREBASE_CHAVE_SERVIDOR')),
        'Content-Type':'application/json'
    }

    body = {
        'to':fcm_token,
        'collapse_key':'type_a',
        'notification':{
            'title':title,
            'body':body
        },
        'data':{
            'body':body,
            'title':title,
            'extra':extra_data,
        }
    }

    try:
        r = requests.post('https://fcm.googleapis.com/fcm/send',headers=headers,json=body)
        response_json = r.json()
        if response_json['sucess'] == 1:
            return {'status':True,'messagem':'success','extra_data':response_json}
    except Exception as e:
        print(str(e))
        return {'status':False,'extra_data':str(e)}