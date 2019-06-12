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

function list_cidade(nome_campo){

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/cidades/",
    })
        .done(function(data) {
            $('#id_cidade').html('');
            $('#id_bairro').html('');
            data.results.forEach((cidade) => {
                $(nome_campo).append(new Option(cidade.nome, cidade.ibge));
            });
        })
        .fail( function(xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
}

/*
cargo: null
celular: null
cpf: "00000000000"
data_atualizacao: "2018-09-26T09:49:15.373119"
data_nascimento: null
endereco: {id: 14, cidade: {…}, data_atualizacao: 1510702970580, cep: "64078270", logradouro: "Rua jose ebaid", …}
farmacia: 10
id: 12
rg: "00000000000"
telefone: "00000000000"
*/
function get_representante(id){

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: `/representante_legal/${id}`,
    })
        .done(function(data) {

            console.log(data);

            $('#rep-nome').val(data.usuario.nome);
            $('#rep-sobrenome').val(data.usuario.sobrenome);
            if(data.cargo != null){
                $('#rep-cargo').val(data.cargo);
            }
            $('#rep-rg').val(data.rg);
            $('#rep-cpf').val(data.cpf);
            $('#rep-telefone').val(data.telefone);
            $('#rep-email').val(data.usuario.email);

            $('#rep-end-cep').val(data.endereco.cep);
            $('#rep-end-logradouro').val(data.endereco.logradouro);
            $('#rep-end-numero').val(data.endereco.numero);
            $('#rep-end-complemento').val(data.endereco.complemento);

            list_cidade('#rep-end-cidade');

            if(data.cargo != null){
                $('#rep-cargo').val(data.cargo);
            }
            if($('#rep-telefone').val().length <= 10){
                $('#rep-telefone').mask('(00) 0000-0000');
            }else{
                $('#rep-telefone').mask('(00) 00000-0000');
            }
            $('#rep-end-cep').mask('00000-000', {reverse: true});
            $('#rep-cpf').mask('000.000.000-00', {reverse: true});

            setTimeout(() =>{ 
                $('#rep-end-cidade').val(data.endereco.cidade).trigger('change');
            }, 400);

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

function update_representante(id, data, success_url){
    let crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    let headers = {"X-CSRFToken": crf_token};
    $.ajax({
        type: "PATCH",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        headers: headers,
        url:`/representante_legal/${id}/`,
    })
        .done(function(data) {
            //location.href = success_url;
            $('#representanteEdit').modal('hide');
            $('.alert-js').show();
            $('#name-detail').text($('#rep-nome').val());
            setTimeout(() =>{ 
                $('.alert-js').fadeOut(1000);
            }, 5000);            

        })
        .fail( function(xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(textStatus);
            console.log(errorThrown);
        });
}

function get_cidade_id(nome_campo) {
    return ($(nome_campo).val() != '' && $(nome_campo).val() != undefined) ? $(nome_campo).val() : null;
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
            id_cidade: get_cidade_id("#id_cidade")
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

$("#rep-end-bairro").select2({
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
            id_cidade: get_cidade_id("#rep-end-cidade")
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
    var pos;
  	$('#edit-farmacia').on('click', function(){
        list_cidade('#id_cidade');
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
    $('#edit-rep').on('click', function(){
        pos = $(this).attr('data-pos');
        get_representante(pos);
    })
    $('#rep-save-edit').on('click', function(){

        $('#rep-telefone').unmask();
        $('#rep-end-cep').unmask();
        $('#rep-cpf').unmask();

        let representante = {};
        representante.usuario = {};
        representante.endereco = {};
        representante.usuario.nome = $('#rep-nome').val();
        representante.usuario.sobrenome = $('#rep-sobrenome').val();
        representante.usuario.email = $('#rep-email').val();
        if($('#rep-cargo').val() != null){
            representante.cargo = $('#rep-cargo').val();
        }
        representante.rg = $('#rep-rg').val();
        representante.cpf = $('#rep-cpf').val();
        representante.telefone = $('#rep-telefone').val();

        representante.endereco.cep = $('#rep-end-cep').val();
        representante.endereco.logradouro = $('#rep-end-logradouro').val();
        representante.endereco.numero = $('#rep-end-numero').val();
        representante.endereco.complemento = $('#rep-end-complemento').val();
        if($('#rep-end-cidade').val()){
            representante.endereco.cidade = $('#rep-end-cidade').val();
        }
        if($('#rep-end-bairro').val()){
            representante.endereco.bairro = $('#rep-end-bairro').val();
        }

        let success_url = "/admin/farmacias/";
        update_representante(pos, representante, success_url);
    });
});
