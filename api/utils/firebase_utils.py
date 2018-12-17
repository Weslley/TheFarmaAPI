from fcm_api import FCMNotification
from core.serializers import ChamadaReduzidaSerializer
from core.models import Configuracoes
from datetime import date, timedelta

def envia_chamada(chamada, fcm_token, numero_cooperativa, time_to_live=None):
    """
    Notificação de chamada
    :param chamada: Chamada
    :param fcm_token: Token FCM
    :return:
    """
    tipo = "chamada"
    mensagem = '%d' % chamada.id

    # Tratamento de retrocompatibilidade para checar se a chamada eh solicitada e se a
    # versao do app em producao permite recebimento de chamadas e não somente o ID
    config = Configuracoes.objects.first()
    dt_versao = config.data_versao_atual_app_motorista
    tempo = timedelta(days=config.dias_para_atualizacao_forcada_app)
    data_atualizacao = dt_versao + tempo
    if chamada.solicitada:
        mensagem = ChamadaReduzidaSerializer(chamada).data

    return envia(tipo, mensagem, fcm_token, numero_cooperativa, time_to_live)


def envia_mensagem(mensagem, fcm_token, numero_cooperativa, time_to_live=None):
    """
    Notificação do tipo mensagem
    :param mensagem: Mensagem a ser enviada
    :param fcm_token: Token FCM
    :return:
    """
    tipo = 'mensagem'
    return envia(tipo, mensagem, fcm_token, numero_cooperativa, time_to_live)


def envia(tipo, mensagem, fcm_token, numero_cooperativa, time_to_live=None):
    """
    Metodo generico para envio da notificação
    :param tipo: Tipo da mensagem
    :param mensagem: Mensagem
    :param fcm_token: Token FCM
    :param numero_cooperativa: Número da unidade que receberá a mensagem
    :return:
    """
    data = {'tipo': tipo, 'mensagem': mensagem, 'numero_cooperativa':numero_cooperativa}
    try:
        push_service = FCMNotification(api_key="AAAApVlLO5A:APA91bGBzAcEISLPTyY0N79XHvHkKpFNDbtxoPYeafLch-RVzpHOzetDkkcV5DnPKgl0T8Ox8u7egia9Pgt2uUuPDShH2xcO9dk0eZQSK8cCVhsaqEsSCwjyW_wXIKSHXROuhzAaf82he7t6JUv5fF7XZ3IaOLfS9g")
        result = push_service.notify_single_device(registration_id=fcm_token, extra_data=data, time_to_live=time_to_live)
        if 'failure' in result and 'success' in result:
            if result['failure']:
                if 'results' in result:
                    erro = result['results'][0]['error']
                    if erro == 'InvalidRegistration':
                        erro = 'Token FCM inválido'
                    return {'sucesso': False, 'mensagem': erro}
                return {'sucesso': False, 'mensagem': 'Erro não identificado'}
            else:
                return {'sucesso': True, 'mensagem': 'Mensagem enviada'}
        return {'sucesso': False, 'mensagem': 'Erro não identificado'}
    except Exception as err:
        print("--------------")
        print(type(err))
        print(err)
        print("--------------")
        return {'sucesso': False, 'mensagem': err}
