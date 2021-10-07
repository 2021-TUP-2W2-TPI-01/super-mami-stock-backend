# Aca van los metodos referidos a usuarios (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from rest_framework import status
from rest_framework.response import Response
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

        usuario = Usuario()

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


def alta_usuario(request):
    try:
        _username = request.POST['username']
        _password = request.POST['password']
        _email = ""
        _last_name = ""
        _first_name = ""
        try:
            _email = request.POST['email']
            _last_name = request.POST['last_name']
            _first_name = request.POST['_first_name']
        except:
            pass
        try:
            if _username != None and _password != None:
                User.objects.create(username = _username, password = _password,email= _email,
                last_name = _last_name, first_name = _first_name)
                return Response('Usuarios creados correctamente', status=status.HTTP_201_CREATED)
            else:
                return Response('Debe Ingresar los campos obligatorios', status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
                print(ex)
                return Response('Existe un usuario con ese username, reintente', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response('Datos Insuficientes', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
