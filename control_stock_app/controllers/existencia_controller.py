# Aca van los metodos referidos a existencias (obtener todas las existencias)
from ..models import *
from django.db import connection
from ..data_access import db_helper as _db

def obtener_existencias(encargado):
   
    deposito = Depositos.objects.filter(id_encargado = encargado)

    if deposito.count() > 0:
        deposito = deposito[0].id
    else:
        # en este caso, no es un encargado si no otro usuario que tiene asignado la visualizacion del deposito
        deposito = DepositosUsuarios.objects.filter(id_usuario=encargado)
        deposito = deposito[0].id_deposito_id

    existencias = _db.get_data_from_procedure(connection=connection,
                                             proc_name='sp_get_existencias_deposito',
                                             proc_params={
                                                    'p_id_deposito': deposito,
                                                })
    return existencias
    """
    existencias = Existencias.objects.select_related('id_articulo','id_deposito', 'id_lote').filter(id_deposito = deposito[0].id, cantidad__gt = 0).values('id_articulo', 'id_articulo__nombre', 'cantidad')

    lstExistencias = []

    for ex in existencias:
            
        existencia = ExistenciaDto()

        existencia.id_articulo = ex['id_articulo']
        existencia.nombre_articulo = ex['id_articulo__nombre']
        existencia.cantidad = ex['cantidad']

        lstExistencias.append(existencia)
        
    return lstExistencias
    """