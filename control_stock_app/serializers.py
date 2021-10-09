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

        
class EncargadosSerializer(serializers.ModelSerializer):

    class Meta:
        model = EncargadoDto
        fields = '__all__'

