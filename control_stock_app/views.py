from django.db.models.query_utils import RegisterLookupMixin
from logging import fatal
from django.http import response
from django.shortcuts import render
from django.db import connection
import rest_framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.utils.serializer_helpers import ReturnDict
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
from .controllers.deposito_controller import *


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    try:
        _username = request.POST['usuario']
        _password = request.POST['password']

        try:
            _objUser = User.objects.get(username=_username, is_active=True)
            if not check_password(_password, _objUser.password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response('Usuario y/o contraseña incorrectos', status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            return Response('Error al intentar autentificar', status=status.HTTP_400_BAD_REQUEST)

        try:
            _token = Token.objects.get(user=_objUser)
        except Token.DoesNotExist:
            _token = Token.objects.create(user=_objUser)

        _user_info = _db.get_data_from_procedure(connection=connection,
                                                 proc_name='sp_get_user_info',
                                                 proc_params={
                                                     'id': _objUser.id
                                                 })

        if len(_user_info) > 0:
            _user_info = _user_info[0]

        return Response(_user_info, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response('Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# ---------- Gestion de usuarios ----------- #
class Usuario(APIView):
    """
    Acá va el GET, POST, PUT, DELETE de la entidad
    """

    def get(self, request, pk):
        try:
            usuario = obtener_usuario(pk)

            response = UsuarioSerializer(usuario)

            return Response(response.data, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('No fue posible obtener el usuario', status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):

        try:
            usuario = UsuarioDto()

            usuario.nombre = request.POST['nombre']
            usuario.apellido = request.POST['apellido']
            usuario.password = request.POST['password']
            usuario.id_tipo_rol = request.POST['id_tipo_rol']
            flag = request.POST['cambio_password']

            if actualizar_usuario(usuario , pk, flag):
                return Response('Usuario actualizado correctamente', status=status.HTTP_200_OK)
            else:
                return Response('Error en los datos', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response('No fue posible actualizar el usuario', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            _username = request.POST['username']
            _password = request.POST['password']
            _email = ""
            _last_name = ""
            _first_name = ""
            _id_tipo_rol = ""
            try:
                _email = request.POST['email']
            except:
                pass
            try:
                _last_name = request.POST['last_name']
            except:
                pass
            try:
                _first_name = request.POST['first_name']
            except:
                pass
            try:
                _id_tipo_rol = request.POST['id_tipo_rol']
            except:
                pass
            if _username != None and _username != "" and _password != None and _password != "":
                if alta_usuario(username=_username, password=_password, email=_email,
                                    last_name=_last_name, first_name=_first_name, id_tipo_rol = _id_tipo_rol):
                    return Response('Usuario creado correctamente', status=status.HTTP_201_CREATED)
                else:
                    return Response('Existe un usuario con ese username, reintente', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Debe ingresar los campos obligatorios', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response('Datos Insuficientes', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, pk):
        try:
            delete_usuario(pk)

        except:
            return Response('Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Usuario dado de baja exitosamente', status=status.HTTP_200_OK)




@api_view(['GET'])
def get_usuarios(request):
    try:

        usuarios = obtener_usuarios()

        reponse = UserSerializer(usuarios, many=True)

        return Response(reponse.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f'Error: {e}')
        return Response('No fue posible obtener usuarios', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_tipos_rol(request):

    try:
        roles = obtener_roles()

        response = TiposRolSerializer(roles, many=True)
    except:
        return Response('No fue posible obtener los tipos de rol', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response(response.data, status=status.HTTP_200_OK)
  
  
# ---------- Gestion de depósitos -------------- #
class Deposito(APIView):
    """
    Acá va el GET, POST, PUT, DELETE de la entidad
    """
    def get(self, request, pk):
        
        try:
            deposito = obtener_deposito(pk)

            response = DepositosInsertSerializer(deposito)

            return Response(response.data, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('No fue posible obtener el depósito', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):

        pass

    def post(self, request):
        try:
            deposito = DepositoDtoInsert()

            deposito.nombre = request.POST['nombre']
            deposito.descripcion = ''
            deposito.domicilio = ''
            deposito.barrio = ''
            deposito.id_localidad = None
            deposito.id_encargado = None
            deposito.activo = 1

            try:
                deposito.descripcion = request.POST['descripcion']
            except:
                pass

            try:
                deposito.domicilio = request.POST['domicilio']
            except:
                pass

            try:
                deposito.barrio = request.POST['barrio']
            except:
                pass

            try:
                if request.POST['id_localidad'] != '':
                    deposito.id_localidad = request.POST['id_localidad']
            except:
                pass

            try:
                if request.POST['id_encargado'] != '':
                    deposito.id_encargado = request.POST['id_encargado']
            except:
                pass

            if alta_deposito(deposito):
                return Response('Depósito creado correctamente', status = status.HTTP_201_CREATED)
            else:
                return Response('Error al insertar el depósito', status = status.HTTP_400_BAD_REQUEST)

        except:
            return Response('No fue posbile insertar el depósito', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            delete_deposito(pk)

        except:
            return Response('Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Depósito dado de baja exitosamente', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_depositos(request):
    try:
        depositos = obtener_depositos()

        response = DepositosSerializer(depositos, many=True)
        
    except:
        return Response('No fue posible obtener depositos', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_localidades(request):
    try:
        localidades = obtener_localidades()

        response = LocalidadesSerializer(localidades, many=True)

    except:
        return Response('No fue posible obtener las localidades', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_encargados(request):
    try:
        encargados = obtener_encargados()

        response = EncargadosSerializer(encargados, many=True)

    except:
        return Response('No fue posible obtener los encargados', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status=status.HTTP_200_OK)
