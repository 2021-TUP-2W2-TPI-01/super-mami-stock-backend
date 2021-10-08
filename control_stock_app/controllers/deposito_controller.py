# Aca van los metodos referidos a depósitos (obtener un depósito, obtener todos los depósitos, alta despósito, baja despósito, modificacion despósito)
from django.http import response
from ..models import *


def obtener_localidades():

    localidades = Localidades.objects.all()

    return localidades