# Aca van los metodos referidos a existencias (obtener todas las existencias)
from ..models import *

def obtener_existencias(encargado):

    deposito = Depositos.objects.filter(id_encargado = encargado)
    existencias = Existencias.objects.select_related('id_articulo','id_deposito', 'id_lote').filter(id_deposito = deposito[0].id, cantidad__gt = 0).values('id_articulo', 'id_articulo__nombre', 'cantidad')

    lstExistencias = []

    for ex in existencias:
            
        existencia = ExistenciaDto()

        existencia.id_articulo = ex['id_articulo']
        existencia.nombre_articulo = ex['id_articulo__nombre']
        existencia.cantidad = ex['cantidad']

        lstExistencias.append(existencia)
        
    return lstExistencias