RET_00  = '00'   # Transação autorizada com sucesso.
RET_000 = '000'  # Transação autorizada com sucesso.
RET_01  = '01'   # Transação não autorizada. Referida (suspeita de fraude) pelo banco emissor.
RET_02  = '02'   # Transação não autorizada. Referida (suspeita de fraude) pelo banco emissor.
RET_03  = '03'   # Transação não permitida. Estabelecimento inválido.
RET_04  = '04'   # Transação não autorizada. Cartão bloqueado pelo banco emissor.
RET_05  = '05'   # Transação não autorizada. Não foi possível processar a transação. Questão relacionada a segurança, inadimplencia ou limite do portador.
RET_06  = '06'   # Não foi possível processar a transação. Cartão cancelado permanentemente pelo banco emissor.
RET_07  = '07'   # Transação não autorizada por regras do banco emissor.
RET_08  = '08'   # Transação não autorizada. Código de segurança inválido.
RET_11  = '11'   # Transação autorizada com sucesso.
RET_12  = '12'   # Não foi possível processar a transação. reveja os dados informados e tente novamente.
RET_13  = '13'   # Transação não permitida. Valor da transação Inválido.
RET_14  = '14'   # Transação não autorizada. Cartão inválido. Pode ser bloqueio do cartão no banco emissor, dados incorretos ou tentativas de testes de cartão.  # Use o Algoritmo de Lhum (Mod 10) para evitar transações não autorizadas por esse motivo. Consulte www.cielo.com.br/desenvolvedores para implantar o Algoritmo de Lhum.
RET_15  = '15'   # Banco emissor indisponível ou inexistente.
RET_19  = '19'   # Refaça a transação ou tente novamente mais tarde.
RET_21  = '21'   # Cancelamento não efetuado. Transação não localizada.
RET_22  = '22'   # Parcelamento inválido. Número de parcelas inválidas.
RET_23  = '23'   # Transação não autorizada. Valor da prestação inválido.
RET_24  = '24'   # Quantidade de parcelas inválido.
RET_25  = '25'   # Pedido de autorização não enviou número do cartão.
RET_28  = '28'   # Arquivo temporariamente indisponível.
RET_39  = '39'   # Transação não autorizada. Erro no banco emissor.
RET_41  = '41'   # Transação não autorizada. Cartão bloqueado por perda.
RET_43  = '43'   # Transação não autorizada. Cartão bloqueado por roubo.
RET_51  = '51'   # Transação não autorizada. Limite excedido/sem saldo.
RET_52  = '52'   # Cartão com dígito de controle inválido.
RET_53  = '53'   # Transação não permitida. Cartão poupança inválido.
RET_54  = '54'   # Transação não autorizada. Cartão vencido.
RET_55  = '55'   # Transação não autorizada. Senha inválida.
RET_57  = '57'   # Transação não permitida para o cartão.
RET_58  = '58'   # Transação não permitida. Opção de pagamento inválida.
RET_59  = '59'   # Transação não autorizada. Suspeita de fraude.
RET_60  = '60'   # Transação não autorizada.
RET_61  = '61'   # Banco emissor indisponível.
RET_62  = '62'   # Transação não autorizada. Cartão restrito para uso doméstico.
RET_63  = '63'   # Transação não autorizada. Violação de segurança Transação não autorizada.
RET_64  = '64'   # Transação não autorizada. Valor abaixo do mínimo exigido pelo banco emissor.
RET_65  = '65'   # Transação não autorizada. Excedida a quantidade de transações para o cartão.
RET_67  = '67'   # Transação não autorizada. Cartão bloqueado para compras hoje.
RET_70  = '70'   # Transação não autorizada. Limite excedido/sem saldo.
RET_72  = '72'   # Cancelamento não efetuado. Saldo disponível para cancelamento insuficiente.
RET_74  = '74'   # Transação não autorizada. A senha está vencida.
RET_75  = '75'   # Senha bloqueada. Excedeu tentativas de cartão.
RET_76  = '76'   # Cancelamento não efetuado. Banco emissor não localizou a transação original Cancelamento não efetuado.
RET_77  = '77'   # Cancelamento não efetuado. Não foi localizado a transação original  Cancelamento não efetuado.
RET_78  = '78'   # Transação não autorizada. Cartão bloqueado primeiro uso.
RET_80  = '80'   # Transação não autorizada. Divergencia na data de transação/pagamento.
RET_82  = '82'   # Transação não autorizada. Cartão inválido.  Transação não autorizada.
RET_83  = '83'   # Transação não autorizada. Erro no controle de senhas.
RET_85  = '85'   # Transação não permitida. Falha da operação. Transação não permitida.
RET_86  = '86'   # Transação não permitida. Falha da operação. Transação não permitida.
RET_89  = '89'   # Erro na transação.  Transação não autorizada.
RET_90  = '90'   # Transação não permitida. Falha da operação.
RET_91  = '91'   # Transação não autorizada. Banco emissor temporariamente indisponível.
RET_92  = '92'   # Transação não autorizada. Tempo de comunicação excedido.
RET_93  = '93'   # Transação não autorizada. Violação de regra - Possível erro no cadastro.
RET_96  = '96'   # Falha no processamento. Não foi possível processar a transação.
RET_97  = '97'   # Valor não permitido para essa transação.
RET_98  = '98'   # Sistema/comunicação indisponível.
RET_99  = '99'   # Sistema/comunicação indisponível.
RET_999 = '999'  # Sistema/comunicação indisponível.
RET_AA  = 'AA'   # Tempo Excedido  Tempo excedido na comunicação com o banco emissor.
RET_AC  = 'AC'   # Transação não permitida. Cartão de débito sendo usado com crédito.
RET_AE  = 'AE'   # Tente Mais Tarde    Tempo excedido na comunicação com o banco emissor.
RET_AF  = 'AF'   # Transação não permitida. Falha da operação.
RET_AG  = 'AG'   # Transação não permitida. Falha da operação.
RET_AH  = 'AH'   # Transação não permitida. Cartão de crédito sendo usado com débito.
RET_AI  = 'AI'   # Transação não autorizada. Autenticação não foi realizada.
RET_AJ  = 'AJ'   # Transação não permitida. Transação de crédito ou débito em uma operação que permite apenas Private Label.
RET_AV  = 'AV'   # Transação não autorizada. Dados Inválidos.
RET_BD  = 'BD'   # Transação não permitida. Falha da operação.
RET_BL  = 'BL'   # Transação não autorizada. Limite diário excedido.
RET_BM  = 'BM'   # Transação não autorizada. Cartão Inválido.
RET_BN  = 'BN'   # Transação não autorizada. Cartão ou conta bloqueado.
RET_BO  = 'BO'   # Transação não permitida. Falha da operação.
RET_BP  = 'BP'   # Transação não autorizada. Conta corrente inexistente.
RET_BV  = 'BV'   # Transação não autorizada. Cartão vencido.
RET_CF  = 'CF'   # Transação não autorizada.C79:J79 Falha na validação dos dados.
RET_CG  = 'CG'   # Transação não autorizada. Falha na validação dos dados.
RET_DA  = 'DA'   # Transação não autorizada. Falha na validação dos dados.
RET_DF  = 'DF'   # Transação não permitida. Falha no cartão ou cartão inválido.
RET_DM  = 'DM'   # Transação não autorizada. Limite excedido/sem saldo.
RET_DQ  = 'DQ'   # Transação não autorizada. Falha na validação dos dados.
RET_DS  = 'DS'   # Transação não permitida para o cartão.
RET_EB  = 'EB'   # Transação não autorizada. Limite diário excedido.
RET_EE  = 'EE'   # Transação não permitida. Valor da parcela inferior ao mínimo permitido.
RET_EK  = 'EK'   # Transação não permitida para o cartão.
RET_FA  = 'FA'   # Transação não autorizada.   Transação não autorizada AmEx.
RET_FC  = 'FC'   # Transação não autorizada. Ligue Emissor Transação não autorizada.
RET_FD  = 'FD'   # Transação negada. Reter cartão condição especial
RET_FE  = 'FE'   # Transação não autorizada. Divergencia na data de transação/pagamento.
RET_FF  = 'FF'   # Cancelamento OK Transação de cancelamento autorizada com sucesso.
RET_FG  = 'FG'   # Transação não autorizada. Ligue AmEx.
RET_FG  = 'FG'   # Ligue 08007285090   Transação não autorizada.
RET_GA  = 'GA'   # Aguarde Contato Transação não autorizada.
RET_HJ  = 'HJ'   # Transação não permitida. Código da operação inválido.
RET_IA  = 'IA'   # Transação não permitida. Indicador da operação inválido.
RET_JB  = 'JB'   # Transação não permitida. Valor da operação inválido.
RET_KA  = 'KA'   # Transação não permitida. Falha na validação dos dados.
RET_KB  = 'KB'   # Transação não permitida. Selecionado a opção incorrente.
RET_KE  = 'KE'   # Transação não autorizada. Falha na validação dos dados.
RET_N7  = 'N7'   # Transação não autorizada. Código de segurança inválido.
RET_R1  = 'R1'   # Transação não autorizada. Cartão inadimplente.
RET_U3  = 'U3'   # Transação não permitida. Falha na validação dos dados.


CHOICES = (
    (RET_00,  'Transação autorizada com sucesso.'),
    (RET_000, 'Transação autorizada com sucesso.'),
    (RET_01,  'Transação não autorizada. Referida (suspeita de fraude) pelo banco emissor.'),
    (RET_02,  'Transação não autorizada. Referida (suspeita de fraude) pelo banco emissor.'),
    (RET_03,  'Transação não permitida. Estabelecimento inválido.'),
    (RET_04,  'Transação não autorizada. Cartão bloqueado pelo banco emissor.'),
    (RET_05,  'Transação não autorizada. Não foi possível processar a transação. Questão relacionada a segurança, inadimplencia ou limite do portador.'),
    (RET_06,  'Não foi possível processar a transação. Cartão cancelado permanentemente pelo banco emissor.'),
    (RET_07,  'Transação não autorizada por regras do banco emissor.'),
    (RET_08,  'Transação não autorizada. Código de segurança inválido.'),
    (RET_11,  'Transação autorizada com sucesso.'),
    (RET_12,  'Não foi possível processar a transação. reveja os dados informados e tente novamente.'),
    (RET_13,  'Transação não permitida. Valor da transação Inválido.'),
    (RET_14,  'Transação não autorizada. Cartão inválido. Pode ser bloqueio do cartão no banco emissor, dados incorretos ou tentativas de testes de cartão.  # Use o Algoritmo de Lhum (Mod 10) para evitar transações não autorizadas por esse motivo. Consulte www.cielo.com.br/desenvolvedores para implantar o Algoritmo de Lhum.'),
    (RET_15,  'Banco emissor indisponível ou inexistente.'),
    (RET_19,  'Refaça a transação ou tente novamente mais tarde.'),
    (RET_21,  'Cancelamento não efetuado. Transação não localizada.'),
    (RET_22,  'Parcelamento inválido. Número de parcelas inválidas.'),
    (RET_23,  'Transação não autorizada. Valor da prestação inválido.'),
    (RET_24,  'Quantidade de parcelas inválido.'),
    (RET_25,  'Pedido de autorização não enviou número do cartão.'),
    (RET_28,  'Arquivo temporariamente indisponível.'),
    (RET_39,  'Transação não autorizada. Erro no banco emissor.'),
    (RET_41,  'Transação não autorizada. Cartão bloqueado por perda.'),
    (RET_43,  'Transação não autorizada. Cartão bloqueado por roubo.'),
    (RET_51,  'Transação não autorizada. Limite excedido/sem saldo.'),
    (RET_52,  'Cartão com dígito de controle inválido.'),
    (RET_53,  'Transação não permitida. Cartão poupança inválido.'),
    (RET_54,  'Transação não autorizada. Cartão vencido.'),
    (RET_55,  'Transação não autorizada. Senha inválida.'),
    (RET_57,  'Transação não permitida para o cartão.'),
    (RET_58,  'Transação não permitida. Opção de pagamento inválida.'),
    (RET_59,  'Transação não autorizada. Suspeita de fraude.'),
    (RET_60,  'Transação não autorizada.'),
    (RET_61,  'Banco emissor indisponível.'),
    (RET_62,  'Transação não autorizada. Cartão restrito para uso doméstico.'),
    (RET_63,  'Transação não autorizada. Violação de segurança Transação não autorizada.'),
    (RET_64,  'Transação não autorizada. Valor abaixo do mínimo exigido pelo banco emissor.'),
    (RET_65,  'Transação não autorizada. Excedida a quantidade de transações para o cartão.'),
    (RET_67,  'Transação não autorizada. Cartão bloqueado para compras hoje.'),
    (RET_70,  'Transação não autorizada. Limite excedido/sem saldo.'),
    (RET_72,  'Cancelamento não efetuado. Saldo disponível para cancelamento insuficiente.'),
    (RET_74,  'Transação não autorizada. A senha está vencida.'),
    (RET_75,  'Senha bloqueada. Excedeu tentativas de cartão.'),
    (RET_76,  'Cancelamento não efetuado. Banco emissor não localizou a transação original Cancelamento não efetuado.'),
    (RET_77,  'Cancelamento não efetuado. Não foi localizado a transação original  Cancelamento não efetuado.'),
    (RET_78,  'Transação não autorizada. Cartão bloqueado primeiro uso.'),
    (RET_80,  'Transação não autorizada. Divergencia na data de transação/pagamento.'),
    (RET_82,  'Transação não autorizada. Cartão inválido.  Transação não autorizada.'),
    (RET_83,  'Transação não autorizada. Erro no controle de senhas.'),
    (RET_85,  'Transação não permitida. Falha da operação. Transação não permitida.'),
    (RET_86,  'Transação não permitida. Falha da operação. Transação não permitida.'),
    (RET_89,  'Erro na transação.  Transação não autorizada.'),
    (RET_90,  'Transação não permitida. Falha da operação.'),
    (RET_91,  'Transação não autorizada. Banco emissor temporariamente indisponível.'),
    (RET_92,  'Transação não autorizada. Tempo de comunicação excedido.'),
    (RET_93,  'Transação não autorizada. Violação de regra - Possível erro no cadastro.'),
    (RET_96,  'Falha no processamento. Não foi possível processar a transação.'),
    (RET_97,  'Valor não permitido para essa transação.'),
    (RET_98,  'Sistema/comunicação indisponível.'),
    (RET_99,  'Sistema/comunicação indisponível.'),
    (RET_999, 'Sistema/comunicação indisponível.'),
    (RET_AA,  'Tempo Excedido  Tempo excedido na comunicação com o banco emissor.'),
    (RET_AC,  'Transação não permitida. Cartão de débito sendo usado com crédito.'),
    (RET_AE,  'Tente Mais Tarde    Tempo excedido na comunicação com o banco emissor.'),
    (RET_AF,  'Transação não permitida. Falha da operação.'),
    (RET_AG,  'Transação não permitida. Falha da operação.'),
    (RET_AH,  'Transação não permitida. Cartão de crédito sendo usado com débito.'),
    (RET_AI,  'Transação não autorizada. Autenticação não foi realizada.'),
    (RET_AJ,  'Transação não permitida. Transação de crédito ou débito em uma operação que permite apenas Private Label.'),
    (RET_AV,  'Transação não autorizada. Dados Inválidos.'),
    (RET_BD,  'Transação não permitida. Falha da operação.'),
    (RET_BL,  'Transação não autorizada. Limite diário excedido.'),
    (RET_BM,  'Transação não autorizada. Cartão Inválido.'),
    (RET_BN,  'Transação não autorizada. Cartão ou conta bloqueado.'),
    (RET_BO,  'Transação não permitida. Falha da operação.'),
    (RET_BP,  'Transação não autorizada. Conta corrente inexistente.'),
    (RET_BV,  'Transação não autorizada. Cartão vencido.'),
    (RET_CF,  'Transação não autorizada.C79:J79 Falha na validação dos dados.'),
    (RET_CG,  'Transação não autorizada. Falha na validação dos dados.'),
    (RET_DA,  'Transação não autorizada. Falha na validação dos dados.'),
    (RET_DF,  'Transação não permitida. Falha no cartão ou cartão inválido.'),
    (RET_DM,  'Transação não autorizada. Limite excedido/sem saldo.'),
    (RET_DQ,  'Transação não autorizada. Falha na validação dos dados.'),
    (RET_DS,  'Transação não permitida para o cartão.'),
    (RET_EB,  'Transação não autorizada. Limite diário excedido.'),
    (RET_EE,  'Transação não permitida. Valor da parcela inferior ao mínimo permitido.'),
    (RET_EK,  'Transação não permitida para o cartão.'),
    (RET_FA,  'Transação não autorizada.   Transação não autorizada AmEx.'),
    (RET_FC,  'Transação não autorizada. Ligue Emissor Transação não autorizada.'),
    (RET_FD,  'Transação negada. Reter cartão condição especial'),
    (RET_FE,  'Transação não autorizada. Divergencia na data de transação/pagamento.'),
    (RET_FF,  'Cancelamento OK Transação de cancelamento autorizada com sucesso.'),
    (RET_FG,  'Transação não autorizada. Ligue AmEx.'),
    (RET_FG,  'Ligue 08007285090   Transação não autorizada.'),
    (RET_GA,  'Aguarde Contato Transação não autorizada.'),
    (RET_HJ,  'Transação não permitida. Código da operação inválido.'),
    (RET_IA,  'Transação não permitida. Indicador da operação inválido.'),
    (RET_JB,  'Transação não permitida. Valor da operação inválido.'),
    (RET_KA,  'Transação não permitida. Falha na validação dos dados.'),
    (RET_KB,  'Transação não permitida. Selecionado a opção incorrente.'),
    (RET_KE,  'Transação não autorizada. Falha na validação dos dados.'),
    (RET_N7,  'Transação não autorizada. Código de segurança inválido.'),
    (RET_R1,  'Transação não autorizada. Cartão inadimplente.'),
    (RET_U3,  'Transação não permitida. Falha na validação dos dados.')
)
