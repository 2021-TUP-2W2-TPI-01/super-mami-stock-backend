from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import model_meta

from control_stock_app.models import TiposRol

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class TiposRolSerializer(serializers.ModelSerializer):

    class Meta:
        model = TiposRol
        fields = '__all__'