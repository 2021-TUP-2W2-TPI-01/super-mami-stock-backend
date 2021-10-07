from django.shortcuts import render
from django.db import connection
import rest_framework
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .serializers import *
from .data_access import db_helper as _db
from .models import *
from rest_framework.authtoken.models import Token
from .controllers.usuario_controller import *

@api_view(['POST'])
def login(request):
    try:
        _username = request.POST['username']
        _password = request.POST['password']

        try:
            _objUser = User.objects.get(username=_username)
            if not check_password(_password, _objUser.password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response('Usuario y/o contraseña incorrectos', status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            return Response('Error al intentar autentificar', status=status.HTTP_400_BAD_REQUEST)

        _user_info = _db.get_data_from_procedure(connection=connection,
                                                 proc_name='sp_get_user_info')
        _response = UserSerializer(_objUser, many=False)

        return Response(_user_info, status=status.HTTP_200_OK)
    except:
        return Response('Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------- Gestion de usuarios ----------- #
class Usuario(APIView):
    """
    Acá va el GET, POST, PUT, DELETE de la entidad
    """

    def get(self, request, pk): 
        
        pass

    def put(self, request, pk):

        pass

    def post(self, request):
        return alta_usuario(request)
    def delete(self, request, pk):

        pass

@api_view(['GET'])
def get_usuarios(request):
    try:

        usuarios = obtener_usuarios()

        reponse = UserSerializer(usuarios, many=True)

        return Response(reponse.data, status=status.HTTP_200_OK)
    except Exception as e:
        print (f'Error: {e}' )
        return Response('No fue posible obtener usuarios', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------------------------- #