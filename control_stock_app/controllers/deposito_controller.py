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

def obtener_deposito(pk):

    deposito = Depositos.objects.get(id = pk)
    encargado = RolesUsuarios.objects.get(id_usuario = deposito.id_encargado)
    localidad = Localidades.objects.get(id = deposito.id_localidad.id)

    dep = DepositoDtoInsert()

    dep.nombre = deposito.nombre
    dep.descripcion = deposito.descripcion
    dep.id_encargado = encargado.id_usuario.id
    dep.domicilio = deposito.domicilio
    dep.barrio = deposito.barrio
    dep.id_localidad = localidad.id
    
    return dep

def actualizar_deposito(deposito, pk):
    try:
        Depositos.objects.filter(id = pk).update(nombre = deposito.nombre, descripcion = deposito.descripcion, domicilio = deposito.domicilio, barrio = deposito.barrio, id_localidad = deposito.id_localidad, id_encargado = deposito.id_encargado)
        return True
    except Exception as e:
        print(e)
        return False


def validar_nombre_deposito_update(nom, id_dep):
    validado = False

    deposito = Depositos.objects.get(id=id_dep)

    # si lo que se está intentando modificar es el nombre, hacemos la validación de disponibilidad de nombres
    if deposito.nombre != nom:

        dep_disponible = Depositos.objects.filter(nombre=nom)

        if dep_disponible.count() == 0:
            validado = True
        
    # si no se está intentando modificar el nombre, lo damos como validado.
    else:
        validado = True
    
    return validado


def validar_nombre_deposito_insert(nom):

    deposito = Depositos.objects.filter(nombre = nom)

    if deposito.count() > 0:
        return False
    else:
        return True


def obtener_deposito_usuario(user):
    try:
        deposito_id = Depositos.objects.get(id_encargado=user).id

        deposito = obtener_deposito(deposito_id)

        return deposito

    except Exception as e:
        print(e)
        return None