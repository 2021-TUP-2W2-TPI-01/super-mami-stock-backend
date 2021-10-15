# Aca van los metodos referidos a traspasos (obtener todas las existencias)
from ..models import *

def alta_traspaso(traspaso, detalle_traspaso):
    try:

        deposito_origen = Depositos.objects.get(id = traspaso.id_deposito_origen)

        deposito_destino = Depositos.objects.get(id = traspaso.id_deposito_destino)

        ultimo_traspaso = Traspasos.objects.create(fh_generacion = datetime.now(), id_tipo_estado_id = 1, id_deposito_origen = deposito_origen, id_deposito_destino = deposito_destino, id_usuario_genero_id = traspaso.id_usuario_genero)

        lstDetalles = []

        for detalle in detalle_traspaso:
            id_articulo = detalle['id_articulo']
            cantidad_articulo = detalle['cantidad']

            det_traspaso = DetallesTraspaso()

            det_traspaso.id_articulo_id = id_articulo
            det_traspaso.cantidad = cantidad_articulo

            det_traspaso.id_traspaso = ultimo_traspaso

            lstDetalles.append(det_traspaso)
        
        DetallesTraspaso.objects.bulk_create(lstDetalles)      
    
        return True

    except Exception as e:
        print(e)
        return False
