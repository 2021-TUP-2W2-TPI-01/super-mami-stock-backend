# Aca van los metodos referidos a artículos (obtener un usuario, obtener todos los usuarios, alta usuario, baja usuario, modificacion usuario)
from ..models import *


def obtener_articulos():
    articulos = Articulos.objects.select_related('id_marca', 'id_categoria', 'id_unidades_medida').filter(activo = True).values('id', 'nombre',
        'descripcion', 'precio_unitario', 'id_marca__descripcion', 'id_categoria__descripcion', 'id_unidad_medida__descripcion', 'cantidad_medida') 

    lstArticulos = []

    for art in articulos:
        articulo = ArticuloDto()

        articulo.id = art['id']
        articulo.nombre = art['nombre']
        
        if art['descripcion'] != None:
            articulo.descripcion = art['descripcion']
        else:
            articulo.descripcion = '-'
        
        articulo.precio_unitario = art['precio_unitario']
        articulo.marca = art['id_marca__descripcion']
        articulo.categoria = art['id_categoria__descripcion']
        articulo.unidad_medida = art['id_unidad_medida__descripcion']
        articulo.cantidad_medida = art['cantidad_medida']

        lstArticulos.append(articulo)

    return lstArticulos


def alta_articulo(articulo):
    try:
        marca = Marcas.objects.get(id = articulo.id_marca)

        categoria = Categorias.objects.get(id = articulo.id_categoria)

        unidad_medida = UnidadesMedida.objects.get(id = articulo.id_unidad_medida)

        Articulos.objects.create(nombre = articulo.nombre, descripcion = articulo.descripcion, precio_unitario = articulo.precio_unitario,
            id_marca = marca, id_categoria = categoria, id_unidad_medida = unidad_medida, cantidad_medida = articulo.cantidad_medida)

        return True
    except Exception as e:
        print(e)
        return False


def articulo_repetido(n):
    if Articulos.objects.filter(nombre = n).count() > 0:
        return True
    else:
        return False


def obtener_marcas():
    marcas = Marcas.objects.all()

    return marcas


def obtener_categorias():
    categorias = Categorias.objects.all()

    return categorias


def obtener_unidades_medida():
    unidades_medida = UnidadesMedida.objects.all()

    return unidades_medida

def delete_articulo(pk):
    Articulos.objects.filter(id = pk).update(activo = 0)