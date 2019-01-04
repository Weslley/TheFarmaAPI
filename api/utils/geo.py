from api.utils.db_work import dictfetchall
from django.db import connection

def get_pedidos_in_radius(latitude,longitude,radius,data_inicio,data_final,farmacia_id,status):
    """
    latitude: Float
    longitudade: Float
    radius: Float
    management_value: Float
    rejecteds: Array
    Status: Int
    return: String

    retorna os vehicle no raio
    """
    sql = """
    SELECT  po_id, nome_produto, nome_fabricante, codigo_barras,count(*)  FROM 
    (SELECT api_pedido.id as p_id, api_produto.id as po_id, api_apresentacao.codigo_barras ,api_produto.nome as nome_produto, api_fabricante.nome as nome_fabricante , api_pedido.data_criacao, api_apresentacao.id as a_id, api_pedido.farmacia_id , api_pedido.status,api_itempedido.id as i_id ,(6371 * acos(CAST((cos(radians({latitude})) * cos(radians(latitude)) *
    cos(radians(longitude) - radians({longitude})) + sin(radians({latitude})) * sin(radians(latitude))) AS DECIMAL)))
    AS distance
    FROM api_pedido
    INNER JOIN api_itempedido ON api_itempedido.pedido_id=api_pedido.id
	INNER JOIN api_apresentacao ON api_apresentacao.id=api_itempedido.apresentacao_id
	INNER JOIN api_produto ON api_produto.id = api_apresentacao.produto_id
	INNER JOIN api_fabricante ON api_fabricante.id = api_produto.laboratorio_id) AS distances
    WHERE distance < {radius} AND data_criacao BETWEEN '{data_inicio}' and '{data_final}' and farmacia_id = {farmacia_id} and status = {status}
    GROUP BY distances.nome_produto, distances.nome_fabricante, codigo_barras, po_id
	ORDER BY distances.count DESC
    OFFSET 0;
    """.format(latitude=latitude,longitude=longitude,radius=radius,data_inicio=data_inicio.strftime('%Y-%m-%d'),data_final=data_final.strftime('%Y-%m-%d'),farmacia_id=farmacia_id,status=status)
    #instancia o cursor
    cursor = connection.cursor()
    #tenta recuperar
    try:
        cursor.execute(sql)
        #retorna o cursor em dict
        dict_curso = dictfetchall(cursor)
    finally:
        cursor.close()
    #retorna
    return dict_curso