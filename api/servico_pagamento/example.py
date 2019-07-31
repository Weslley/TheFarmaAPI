from datetime import datetime
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api.servico_pagamento import tipo_servicos
from api.servico_pagamento.pagamento import Pagamento
from api.servico_pagamento.servicos.cielo import ServicoCielo, ResponseCieloException
from api.utils import status_transacao_cartao_cielo


def processa_cielo(self, data):
    try:
        with transaction.atomic():
            venda = object
            # data['venda'] = venda = VendaCartao.objects.create(
            #     motorista=data['unidade'].motorista,
            #     unidade=data['unidade'],
            #     descricao='RADIO TAXI',
            #     valor=data['valor'],
            #     bandeira=self.translate_brand(data['bandeira'])
            # )
            data = Pagamento.pagar(tipo_servicos.CIELO, data)

            json_venda, json_captura = data['venda'], data['captura']

            venda.pagamento_status = int(json_venda['Payment']['Status'])
            venda.pagamento_numero_autorizacao = int(json_venda['Payment']['ProofOfSale']) if 'ProofOfSale' in \
                                                                                              json_venda[
                                                                                                  'Payment'] else None
            venda.pagamento_id = json_venda['Payment']['PaymentId']
            venda.pagamento_data_recebimento = datetime.strptime(json_venda['Payment']['ReceivedDate'],
                                                                 '%Y-%m-%d %H:%M:%S')
            venda.pagamento_codigo_autorizacao = json_venda['Payment']['AuthorizationCode'] if 'AuthorizationCode' in \
                                                                                               json_venda[
                                                                                                   'Payment'] else None
            venda.pagamento_tid = str(json_venda['Payment']['Tid'])
            venda.pagamento_mensagem_retorno = json_venda['Payment']['ReturnMessage']
            venda.pagamento_codigo_retorno = json_venda['Payment']['ReturnCode']

            if json_captura:
                venda.capturado = True
                venda.captura_status = int(json_captura['Status'])
                venda.captura_codigo_retorno = json_captura['ReturnCode']
                venda.captura_mensagem_retorno = json_captura['ReturnMessage']

            venda.status = ServicoCielo.status_pagamento(venda.pagamento_id)
            venda.save()

            if venda.pagamento_status == status_transacao_cartao_cielo.AUTHORIZED and venda.captura_status == status_transacao_cartao_cielo.PAYMENT_CONFIRMED:
                return Response({'retorno': 'Transação aprovada - NSU: {}'.format(venda.pagamento_numero_autorizacao)},
                                status=status.HTTP_200_OK)
            else:
                return Response({'retorno': 'Transação não aprovada'}, status=status.HTTP_200_OK)
    except ResponseCieloException as err:
        return Response({'retorno': str(err)}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        print(type(e))
        return Response({'retorno': 'Erro ao processar o pagamento.'}, status=status.HTTP_200_OK)