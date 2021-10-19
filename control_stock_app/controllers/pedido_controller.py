# Aca van los metodos referidos a pedidos (obtener un pedido, obtener todos los pedidos y la confirmación de los tres estados de pedidos (confirmado, modificado y rechazado))
from ..models import *

def obtener_pedidos(usuario):

    depositoUsuario = Depositos.objects.get(id_encargado = usuario)

    pedidos = Pedidos.objects.select_related('id_proveedor', 'id_tipo_estado', 'id_deposito_destino').filter(id_deposito_destino=depositoUsuario).values('id',
     'fecha', 'numero_remito_asociado', 'id_tipo_estado__descripcion', 'id_proveedor__descripcion', 'id_deposito_destino__nombre')

    lstPedidos = []

    for p in pedidos:
        pedido = PedidoDto()

        pedido.id = p['id']
        pedido.fecha = p['fecha']
        pedido.numero_remito_asociado = p['numero_remito_asociado']
        pedido.tipo_estado = p['id_tipo_estado__descripcion']
        pedido.proveedor = p['id_proveedor__descripcion']
        pedido.deposito_destino = p['id_deposito_destino__nombre']

        lstPedidos.append(pedido)

    return lstPedidos


def obtener_pedido(pk):

    pedido = Pedidos.objects.select_related('id_proveedor', 'id_tipo_estado', 'id_deposito_destino','id_usuario_proceso').filter(id = pk).values('id',
     'fecha', 'numero_remito_asociado', 'id_tipo_estado__descripcion', 'observaciones', 'id_proveedor__descripcion', 'id_deposito_destino__nombre', 'fh_procesado', 'id_usuario_proceso','id_usuario_proceso__first_name','id_usuario_proceso__last_name')

    detalles_pedido = DetallesPedido.objects.select_related('id_pedido', 'id_articulo').filter(id_pedido = pk).values('id', 'id_articulo__id', 'id_articulo__nombre', 'cantidad')

    p = PedidoDto()

    p.id = pedido[0]['id']
    p.fecha = pedido[0]['fecha']
    p.numero_remito_asociado = pedido[0]['numero_remito_asociado']
    p.tipo_estado = pedido[0]['id_tipo_estado__descripcion']
    p.observaciones = pedido[0]['observaciones']
    p.proveedor = pedido[0]['id_proveedor__descripcion']
    p.deposito_destino = pedido[0]['id_deposito_destino__nombre']

    if pedido[0]['fh_procesado'] is not None:
        p.fh_procesado = pedido[0]['fh_procesado']

    if pedido[0]['id_usuario_proceso'] is not None:
        p.usuario_proceso = f'{pedido[0]["id_usuario_proceso__first_name"]} {pedido[0]["id_usuario_proceso__last_name"]}'
    
    
    p.detalles_pedido = list(detalles_pedido)

    return p


def armado_lista(pk, detalles_pedido):
    pedido = Pedidos.objects.get(id = pk)

    lst_detalles_pedido = []

    for detalle in detalles_pedido:
        det_ped = DetallesPedido()

        det_ped.id_pedido = pedido
        det_ped.id_articulo_id = detalle['id_articulo']
        det_ped.cantidad = detalle['cantidad']

        lst_detalles_pedido.append(det_ped)

    return lst_detalles_pedido


def delete_detalles_pedido(pk):
    try:
        DetallesPedido.objects.filter(id_pedido = pk).delete()
    except Exception as e:
        print(e)
        return False

    return True


def insert_detalles_pedido(lst_detalles_pedido):
    DetallesPedido.objects.bulk_create(lst_detalles_pedido)