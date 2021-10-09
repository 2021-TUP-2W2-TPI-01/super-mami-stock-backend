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

  
def delete_deposito(pk):

    Depositos.objects.filter(id = pk).update(activo = 0)



def obtener_localidades():

    localidades = Localidades.objects.all()

    return localidades


def obtener_encargados():

    encargados = RolesUsuarios.objects.select_related('id_usuario').filter(id_tipo_rol=3).values('id_usuario', 'id_usuario__first_name', 'id_usuario__last_name')

    lstEncargados = []

    for e in encargados:

        encargado = EncargadoDto()

        encargado.id = e['id_usuario']

        if e['id_usuario__first_name'] != None and e['id_usuario__last_name'] != None:
            encargado.descripcion = e['id_usuario__first_name'] + ' ' + e['id_usuario__last_name']
        else:
            encargado.descripcion = '-'

        lstEncargados.append(encargado)

    return lstEncargados