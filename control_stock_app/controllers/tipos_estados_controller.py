from ..models import *


def obtener_tipos_estados():
    tipos_estados = TiposEstado.objects.all()

    return tipos_estados