/* 
* Retorna um JSON com os campos do formulário
*/
function desabilitaMascaras(){
    $('#id_cnpj').unmask();
    $('#id_telefone').unmask();
    $('#id_cep').unmask();
}

function getCampos(){

    desabilitaMascaras();

    let farmacia = {};
    farmacia.endereco = {};
    farmacia.conta_bancaria = {};

    //Campos da aba DADOS BASICO
    farmacia.razao_social = $('#id_razao_social').val();
    farmacia.nome_fantasia = $('#id_nome_fantasia').val();
    farmacia.cnpj = $('#id_cnpj').val();
    farmacia.telefone = $('#id_telefone').val();
    //Campos da aba ENDERECO
    farmacia.endereco.cep = $('#id_cep').val();
    farmacia.endereco.logradouro = $('#id_logradouro').val();
    farmacia.endereco.numero = $('#id_numero_end').val();
    farmacia.endereco.complemento = $('#id_complemento').val();
    farmacia.endereco.cidade = $('#id_cidade').val();
    farmacia.endereco.bairro = $('#id_bairro').val();
    //Campos da aba CONTA BANCARIA
    $('#id_banco').val();
    farmacia.conta_bancaria.numero_agencia = $('#id_num_agencia').val();
    farmacia.conta_bancaria.digito_agencia = $('#id_dig_agencia').val();
    farmacia.conta_bancaria.numero_conta = $('#id_num_conta').val();
    farmacia.conta_bancaria.digito_conta = $('#id_dig_conta').val();
    farmacia.conta_bancaria.operacao = $('#id_operacao').val();
    //Campos da aba PEDIDOS
    farmacia.servico_entregador = $('#possui_entregador').prop('checked');
    farmacia.servico_estoque = $('#habilitar_estoque').prop('checked');
    farmacia.percentual_similar = $('#perc_similares').val().replace(',', '.');
    farmacia.percentual_generico = $('#perc_genericos').val().replace(',', '.');
    farmacia.percentual_etico = $('#perc_eticos').val().replace(',', '.');
    farmacia.nao_medicamentos = $('#perc_nao_medic').val().replace(',', '.');
    farmacia.horario_funcionamento_segunda_sexta_inicial = $('#horario_diasuteis_inicial').val();
    farmacia.horario_funcionamento_segunda_sexta_final = $('#horario_diasuteis_final').val();
    farmacia.horario_funcionamento_sabado_inicial = $('#horario_sabados_inicial').val();
    farmacia.horario_funcionamento_sabado_final = $('#horario_sabados_final').val();
    farmacia.horario_funcionamento_domingo_inicial = $('#horario_domingos_inicial').val();
    farmacia.horario_funcionamento_domingo_final = $('#horario_domingos_final').val();
    farmacia.horario_funcionamento_feriado_inicial = $('#horario_feriados_inicial').val();
    farmacia.horario_funcionamento_feriado_final = $('#horario_feriados_final').val();
    farmacia.tempo_entrega = $('#tempo_entrega').val();
    farmacia.latitude = $('#latitude').val().replace(',', '.');
    farmacia.longitude = $('#longitude').val().replace(',', '.');

    console.log(farmacia);
  
    return farmacia;
}

function habilitaCampos(){

	//Torna os campos disponiveis para edição;
	//Campos da aba DADOS BASICO
	$('#id_razao_social').prop('disabled', false);
	$('#id_nome_fantasia').prop('disabled', false);
	$('#id_cnpj').prop('disabled', false);
	$('#id_telefone').prop('disabled', false);
	//Campos da aba ENDERECO
	$('#id_cep').prop('disabled', false);
	$('#id_logradouro').prop('disabled', false);
	$('#id_numero_end').prop('disabled', false);
	$('#id_complemento').prop('disabled', false);
	$('#id_cidade').prop('disabled', false);
	$('#id_bairro').prop('disabled', false);
	//Campos da aba CONTA BANCARIA
	$('#id_banco').prop('disabled', false);
	$('#id_num_agencia').prop('disabled', false);
	$('#id_dig_agencia').prop('disabled', false);
	$('#id_num_conta').prop('disabled', false);
	$('#id_dig_conta').prop('disabled', false);
	$('#id_operacao').prop('disabled', false);
	//Campos da aba PEDIDOS
	$('#possui_entregador').prop('disabled', false);
	$('#habilitar_estoque').prop('disabled', false);
	$('#perc_similares').prop('disabled', false);
	$('#perc_genericos').prop('disabled', false);
	$('#perc_eticos').prop('disabled', false);
	$('#perc_nao_medic').prop('disabled', false);
	$('#horario_diasuteis_inicial').prop('disabled', false);
	$('#horario_diasuteis_final').prop('disabled', false);
	$('#horario_sabados_inicial').prop('disabled', false);
	$('#horario_sabados_final').prop('disabled', false);
	$('#horario_domingos_inicial').prop('disabled', false);
	$('#horario_domingos_final').prop('disabled', false);
	$('#horario_feriados_inicial').prop('disabled', false);
	$('#horario_feriados_final').prop('disabled', false);
	$('#tempo_entrega').prop('disabled', false);
	$('#latitude').prop('disabled', false);
	$('#longitude').prop('disabled', false);

}

function list_cidade(){

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/cidades/",
    })
        .done(function(data) {
            $('#id_cidade').html('');
            $('#id_bairro').html('');
            data.results.forEach((cidade) => {
                $('#id_cidade').append(new Option(cidade.nome, cidade.ibge));
            });
        })
        .fail( function(xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
}

function list_banco(){

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/bancos/",
    })
        .done(function(data) {
            data.results.forEach((banco) => {
                $('#id_banco').append(new Option(banco.nome, banco.id));
            });
        })
        .fail( function(xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
}

function update_farmacia(data, url, headers, success_url){
    $.ajax({
        type: "PATCH",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        headers: headers,
        data: JSON.stringify(data),
        url:`${url}`,
    })
        .done(function(data) {
            location.href = success_url;
        })
        .fail( function(xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
}

function get_cidade_id() {
    return ($("#id_cidade").val() != '' && $("#id_cidade").val() != undefined) ? $("#id_cidade").val() : null;
}

$("#id_bairro").select2({
    language: "pt-BR",
    width: '100%',
    ajax: {
        url: "/admin/bairros/busca/",
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            q: params.term, // search term
            page: params.page,
            id_cidade: get_cidade_id()
          };
        },
        processResults: function (data, params) {
          // parse the results into the format expected by Select2
          // since we are using custom formatting functions we do not need to
          // alter the remote JSON data, except to indicate that infinite
          // scrolling can be used
          params.page = params.page || 1;

          return {
            results: data.content.items,
          };
        },
        cache: false
    },
    escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
    minimumInputLength: 3
});

$( document ).ready(function() {
  	$('#edit-farmacia').on('click', function(){
        list_cidade();
        list_banco();
	  	$('#salvar-edit').show();
	  	$('#add-rep').hide();
	  	$('#edit-farmacia').hide();
        setTimeout(() =>{ 
            $('#id_cidade').val('').trigger('change');
            $('#id_bairro').val('').trigger('change');
            $('#id_banco').val('').trigger('change');
        }, 400);
	  	habilitaCampos();
  	});
});
