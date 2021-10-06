# Aca van los metodos referidos a usuarios (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from ..models import *
from django.contrib.auth.models import User

def obtener_usuarios():

    usuarios = User.objects.all()

    return usuarios
    
