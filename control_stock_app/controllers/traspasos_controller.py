from ..models import *
from django.db import connection
from ..data_access import db_helper as _db


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


def obtener_traspasos_al_deposito(usuario):

    lstTraspasos = []

    try:
        depositoUsuario = Depositos.objects.get(id_encargado=usuario)

        traspasos = Traspasos.objects.select_related('id_deposito_origen',
                                                        'id_deposito_destino',
                                                        'id_tipo_estado').filter(id_deposito_destino=depositoUsuario).values('id',
                                                                                                                            'fh_generacion',
                                                                                                                            'id_deposito_origen__nombre',
                                                                                                                            'id_deposito_destino__nombre',
                                                                                                                            'id_tipo_estado__descripcion').order_by('id_tipo_estado','fh_generacion')

        for t in traspasos:
            
            traspaso = TraspasoDto()

            traspaso.id = t['id']
            traspaso.fh_generacion = datetime.strftime(t['fh_generacion'], '%d-%m-%Y %H:%M')
            traspaso.deposito_origen = t['id_deposito_origen__nombre']
            traspaso.deposito_destino = t['id_deposito_destino__nombre']
            traspaso.tipo_estado = t['id_tipo_estado__descripcion']

            lstTraspasos.append(traspaso)

    except Exception as e:
        print(e)
    
    return lstTraspasos


def obtener_traspaso(id):

    lstDetalles = []
    result = {}

    try:
        traspaso = Traspasos.objects.select_related('id_tipo_estado',
                                                    'id_deposito_origen',
                                                    'id_deposito_destino',
                                                    'id_usuario_genero').values('id',
                                                                                'fh_generacion',
                                                                                'id_tipo_estado__descripcion',
                                                                                'id_deposito_origen__nombre',
                                                                                'id_deposito_destino__nombre',
                                                                                'id_usuario_genero__first_name',
                                                                                'id_usuario_genero__last_name', 'id_usuario_proceso__first_name', 'id_usuario_proceso__last_name','fh_procesado', 'observaciones').get(pk=id)

        detalle = DetallesTraspaso.objects.select_related('id_articulo').filter(id_traspaso_id=traspaso['id']).values('id_articulo',
                                                                                                                      'id_articulo__nombre',
                                                                                                                      'cantidad')

        # Serializado a mano
        # -----------------------------------

        for det in detalle:

            lstDetalles.append({
                'id_articulo': det['id_articulo'],
                'articulo': det['id_articulo__nombre'],
                'cantidad': det['cantidad']
            })

        result['id'] = traspaso['id']
        result['fh_generacion'] = traspaso['fh_generacion']
        result['tipo_estado'] = traspaso['id_tipo_estado__descripcion']
        result['deposito_origen'] = traspaso['id_deposito_origen__nombre']
        result['deposito_destino'] = traspaso['id_deposito_destino__nombre']
        result['usuario_genero'] = f'{traspaso["id_usuario_genero__first_name"]} {traspaso["id_usuario_genero__last_name"]}'
        result['usuario_proceso'] = f'{traspaso["id_usuario_proceso__first_name"]} {traspaso["id_usuario_proceso__last_name"]}'
        if traspaso['fh_procesado'] is not None:
            result['fh_procesado'] = traspaso['fh_procesado']
        result['observaciones'] = traspaso['observaciones']

        result['detalle_traspaso'] = lstDetalles

        # -----------------------------------

        return result

    except Exception as e:
        print(e)
        return None


def traspaso_confirmado(id_traspaso, id_usuario):

    resultado = False
    try:

        

        result = _db.get_data_from_procedure(connection=connection,
                                             proc_name='sp_procesar_traspaso_confirmado',
                                             proc_params={
                                                    'p_id_traspaso': id_traspaso,
                                                    'p_id_usuario' : id_usuario
                                                })
        if len(result) > 0:
            result = result[0]['v_result']
        
        if result == 'OK':
            resultado = True
    
    except Exception as e:
        print(e)

    return resultado


def traspaso_modificado(id_usuario, traspasoDto):

    resultado = False
    try:


        lstNuevoDetalle = []

        for det in traspasoDto.detalle_traspaso:
            detalleNuevo = DetallesTraspaso()

            detalleNuevo.id_traspaso_id = traspasoDto.id
            detalleNuevo.id_articulo_id = det['id_articulo']
            detalleNuevo.cantidad = det['cantidad']


            lstNuevoDetalle.append(detalleNuevo)

        DetallesTraspaso.objects.filter(id_traspaso_id=traspasoDto.id).delete()

        DetallesTraspaso.objects.bulk_create(lstNuevoDetalle)

        result = _db.get_data_from_procedure(connection=connection,
                                             proc_name='sp_procesar_traspaso_modificado',
                                             proc_params={
                                                    'p_id_traspaso': traspasoDto.id,
                                                    'p_id_usuario' : id_usuario,
                                                    'p_observacion' : traspasoDto.observaciones
                                                })
        if len(result) > 0:
            result = result[0]['v_result']
        
        if result == 'OK':
            resultado = True
    
    except Exception as e:
        print(e)

    return resultado


def traspaso_rechazado(id_usuario, traspasoDto):

    resultado = False
    try:

        

        result = _db.get_data_from_procedure(connection=connection,
                                             proc_name='sp_procesar_traspaso_rechazado',
                                             proc_params={
                                                    'p_id_traspaso': traspasoDto.id,
                                                    'p_id_usuario' : id_usuario,
                                                    'p_observacion' : traspasoDto.observaciones
                                                })
        if len(result) > 0:
            result = result[0]['v_result']
        
        if result == 'OK':
            resultado = True
    
    except Exception as e:
        print(e)

    return resultado
