from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import model_meta

class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    usuario = serializers.CharField(max_length=150)
    nombre = serializers.CharField(max_length=150)
    apellido = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    ult_conexion = serializers.DateTimeField()
    rol = serializers.CharField(max_length=50)