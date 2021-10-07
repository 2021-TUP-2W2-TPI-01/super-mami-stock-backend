# Aca van los metodos referidos a usuarios (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from rest_framework import status
from rest_framework.response import Response
from ..models import *
from django.contrib.auth.models import User


def obtener_usuarios():

    usuarios = User.objects.all()

    return usuarios


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
