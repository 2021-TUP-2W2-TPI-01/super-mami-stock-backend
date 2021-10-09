# Aca van los metodos referidos a depósitos (obtener un depósito, obtener todos los depósitos, alta despósito, baja despósito, modificacion despósito)
from django.http import response
from ..models import *


def obtener_depositos():

    depositos = Depositos.objects.select_related('id_localidad', 'id_encargado').filter(activo=True).values('id', 'nombre', 'descripcion', 'domicilio', 'barrio', 'id_localidad__descripcion', 'id_encargado__first_name', 'id_encargado__last_name')

    lstDepositos = []

    for d in depositos:

        deposito = DepositoDto()

        deposito.id = d['id']
        deposito.nombre = d['nombre']
        deposito.descripcion = d['descripcion']
        deposito.domicilio = d['domicilio']
        deposito.barrio = d['barrio']
        deposito.localidad = d['id_localidad__descripcion']
        
        if d['id_encargado__first_name'] != None and d['id_encargado__last_name'] != None:
            deposito.encargado = d['id_encargado__first_name'] + ' ' +  d['id_encargado__last_name']
        else:
            deposito.encargado = '-'

        lstDepositos.append(deposito)

    return lstDepositos


def obtener_localidades():

    localidades = Localidades.objects.all()

    return localidades