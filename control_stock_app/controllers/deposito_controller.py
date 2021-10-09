# Aca van los metodos referidos a depósitos (obtener un depósito, obtener todos los depósitos, alta despósito, baja despósito, modificacion despósito)
from django.http import response
from ..models import *


def alta_deposito(deposito):
    """
    _nombre = deposito.nombre
    _descripcion = deposito.descripcion
    _domicilio = deposito.domicilio
    _barrio = deposito.barrio
    _id_localidad = deposito.id_localidad
    _id_encargado = deposito.id_encargado
    _activo = deposito.activo
    """

    try:
        localidad = Localidades.objects.get(id = deposito.id_localidad)
        encargado = User.objects.get(id = deposito.id_encargado)

        Depositos.objects.create(nombre = deposito.nombre, descripcion = deposito.descripcion, domicilio = deposito.domicilio,
        barrio = deposito.barrio, id_localidad = localidad, id_encargado = encargado, activo = deposito.activo)

        return True
    except:
        return False

def obtener_localidades():

    localidades = Localidades.objects.all()

    return localidades