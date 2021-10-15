# Aca van los metodos referidos a pedidos (obtener un pedido, obtener todos los pedidos y la confirmación de los tres estados de pedidos (confirmado, modificado y rechazado))
from ..models import *

def obtener_pedidos():

    pedidos = Pedidos.objects.select_related('id_proveedor', 'id_tipo_estado', 'id_deposito_destino').filter(id_tipo_estado = 1).values('id',
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