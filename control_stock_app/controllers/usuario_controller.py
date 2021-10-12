# Aca van los metodos referidos a usuarios (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from django.contrib.auth.hashers import make_password
from ..models import *
from django.contrib.auth.models import User


def obtener_usuarios():

    usuarios = User.objects.filter(is_active=True).values('id','username','first_name','last_name','email','last_login')

    lstUsuarios = []

    for usr in usuarios:

        rol = RolesUsuarios.objects.select_related('id_tipo_rol').filter(id_usuario=usr['id']).values('id_tipo_rol__descripcion')

        if rol.count() > 0:
            rol = rol[0]['id_tipo_rol__descripcion']
        else:
            rol = ''

        usuario = UsuarioDto()

        usuario.id = usr['id']
        usuario.usuario = usr['username']
        usuario.nombre = usr['first_name']
        usuario.apellido = usr['last_name']
        usuario.email = usr['email']

        try:
            usuario.ult_conexion = datetime.strftime(usr['last_login'],'%d-%m-%Y %H:%m')
        except:
            usuario.ult_conexion = None
        
        usuario.rol = rol

        lstUsuarios.append(usuario)
        

    return lstUsuarios


def alta_usuario(**args):
    _username = args.get('username')
    _password = make_password(args.get('password'))
    _email = args.get('email')
    _last_name = args.get('last_name')
    _first_name = args.get('first_name')
    _id_tipo_rol = args.get('id_tipo_rol')
    try:
        _rol = TiposRol.objects.get(id = _id_tipo_rol)
        _ultimo_usuario = User.objects.create(username = _username, password = _password,email= _email,
        last_name = _last_name, first_name = _first_name)
        RolesUsuarios.objects.create(id_usuario = _ultimo_usuario, id_tipo_rol = _rol)
        return True
    except Exception as e:
        print(e)
        return False


def actualizar_usuario(usuario, pk, flag):
    try:
        usuario.password = make_password(usuario.password)

        if flag == '1':
            User.objects.filter(id = pk).update(first_name = usuario.nombre, last_name = usuario.apellido, password = usuario.password)
        else:
            User.objects.filter(id = pk).update(first_name = usuario.nombre, last_name = usuario.apellido)

        RolesUsuarios.objects.filter(id_usuario = pk).update(id_tipo_rol = usuario.id_tipo_rol)
    
        return True
    except Exception as e:
        print(e)
        return False

def obtener_usuario(pk):
    usuario = User.objects.get(id = pk)
    rol = RolesUsuarios.objects.filter(id_usuario = pk).values('id_tipo_rol')

    usr = UsuarioDto()

    usr.nombre = usuario.first_name
    usr.apellido = usuario.last_name
    usr.usuario = usuario.username
    usr.email = usuario.email
    usr.password = usuario.password
    usr.id_tipo_rol = rol[0]['id_tipo_rol']

    return usr



def obtener_roles():

    roles = TiposRol.objects.all()

    return roles
    
    
def delete_usuario(pk):

    User.objects.filter(id = pk).update(is_active = 0)

