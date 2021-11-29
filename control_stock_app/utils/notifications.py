from ..models import *
import requests
from django.conf import settings

endpointURL = f'{settings.SOCKET_URL}/send-msg-to-user'

def notificar_nuevo_traspaso(traspaso):
    
    try:
        
        user_traspaso_origen = User.objects.get(id=traspaso.id_usuario_genero)
        dep_origen = Depositos.objects.values('nombre').get(id=traspaso.id_deposito_origen)['nombre']
        dep_destino = Depositos.objects.values('id_encargado').get(id=traspaso.id_deposito_destino)
        user_traspaso_destino = User.objects.values('username').get(id=dep_destino['id_encargado'])['username']

        msg = f'{user_traspaso_origen.first_name} {user_traspaso_origen.last_name} ({dep_origen}) ha generado un traspaso hacia tu depósito'

        bodyRequest = {
            'username' : user_traspaso_destino,
            'body' : msg  
        }

        headerRequest = {
            'Content-Type' : 'application/json'
        }

        requests.post(endpointURL, json=bodyRequest, headers=headerRequest)
    except Exception as e:
        print (f'Error al enviar notificación: {e}')


def notificar_procesamiento_traspaso(id_traspaso):

    try:

        traspaso = Traspasos.objects.get(id=id_traspaso)

        usuario_proceso = traspaso.id_usuario_proceso
        usuario_genero = traspaso.id_usuario_genero
        
        sucursal = traspaso.id_deposito_destino

        msg = f'{usuario_proceso.first_name} {usuario_proceso.last_name} ({sucursal.nombre}) ha procesado tu traspaso. El estado del mismo es {traspaso.id_tipo_estado.descripcion}'

        bodyRequest = {
            'username' : usuario_genero.username,
            'body' : msg  
        }

        headerRequest = {
            'Content-Type' : 'application/json'
        }

        requests.post(endpointURL, json=bodyRequest, headers=headerRequest)
    except Exception as e:
        print (f'Error al enviar notificación: {e}')
