# Aca van los metodos referidos a usuarios (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from django.http import response
from ..models import *
from django.contrib.auth.models import User


def obtener_usuarios():

    usuarios = User.objects.all()

    return usuarios


def obtener_roles():

    roles = TiposRol.objects.all()

    return roles


def delete_usuario(pk):

    User.objects.filter(id = pk).update(is_active = 0)