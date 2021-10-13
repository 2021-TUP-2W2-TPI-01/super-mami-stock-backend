# Aca van los metodos referidos a artículos (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from ..models import *

def obtener_marcas():
    marcas = Marcas.objects.all()

    return marcas


def obtener_categorias():
    categorias = Categorias.objects.all()

    return categorias


def obtener_unidades_medida():
    unidades_medida = UnidadesMedida.objects.all()

    return unidades_medida