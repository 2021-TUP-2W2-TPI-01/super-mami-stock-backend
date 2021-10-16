from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.utils import model_meta
from control_stock_app import models
from control_stock_app.models import *




class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    usuario = serializers.CharField(max_length=150)
    nombre = serializers.CharField(max_length=150)
    apellido = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    ult_conexion = serializers.DateTimeField()
    rol = serializers.CharField(max_length=50)


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioDto
        fields = ('usuario', 'nombre', 'apellido', 'email', 'password', 'id_tipo_rol')

    
class TiposRolSerializer(serializers.ModelSerializer):

    class Meta:
        model = TiposRol
        fields = '__all__'


class LocalidadesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Localidades
        fields = '__all__'


class DepositosSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositoDto
        fields = '__all__'


class DepositosInsertSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositoDtoInsert
        fields = ('nombre', 'descripcion', 'domicilio', 'barrio', 'id_localidad', 'id_encargado')


class EncargadosSerializer(serializers.ModelSerializer):

    class Meta:
        model = EncargadoDto
        fields = '__all__'


class ArticulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloDto
        fields = ('id', 'nombre', 'descripcion', 'precio_unitario', 'marca', 'categoria', 'unidad_medida', 'cantidad_medida')


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloDto
        fields = ('nombre', 'descripcion', 'precio_unitario', 'id_marca', 'id_categoria', 'id_unidad_medida', 'cantidad_medida')


class MarcasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marcas
        fields = '__all__'


class CategoriasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorias
        fields = '__all__'


class UnidadesMedidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadesMedida
        fields = '__all__'


class TraspasosSerializer(serializers.ModelSerializer):

    class Meta:
        model = TraspasoDto
        fields = ('id','fh_generacion','deposito_origen','deposito_destino','tipo_estado')


class ExistenciasSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExistenciaDto
        fields = ('id_articulo', 'nombre_articulo','cantidad')

