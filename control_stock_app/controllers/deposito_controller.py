# Aca van los metodos referidos a depósitos (obtener un depósito, obtener todos los depósitos, alta despósito, baja despósito, modificacion despósito)
from django.http import response
from ..models import *


def alta_deposito(deposito):

    try:
        if deposito.id_encargado != None:
            encargado = User.objects.get(id = deposito.id_encargado)
        else:
            encargado = None

        if deposito.id_localidad != None:
            localidad = Localidades.objects.get(id = deposito.id_localidad)
        else:
            localidad = None

        Depositos.objects.create(nombre = deposito.nombre, descripcion = deposito.descripcion, domicilio = deposito.domicilio,
        barrio = deposito.barrio, id_localidad = localidad, id_encargado = encargado, activo = deposito.activo)

        return True
    except Exception as e:
        print(e)
        return False

def obtener_localidades():

    localidades = Localidades.objects.all()

    return localidades