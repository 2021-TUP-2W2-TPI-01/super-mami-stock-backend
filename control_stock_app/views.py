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

from .controllers.traspasos_controller import *
from .serializers import *
from .data_access import db_helper as _db
from .models import *
from rest_framework.authtoken.models import Token
from .controllers.usuario_controller import *
from .controllers.deposito_controller import *
from .controllers.articulo_controller import *
from .controllers.pedido_controller import *
from .controllers.existencia_controller import *



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

        try: 
            deposito = DepositoDtoInsert()

            deposito.nombre = request.POST['nombre']
            deposito.descripcion = request.POST['descripcion']
            deposito.domicilio = request.POST['domicilio']
            deposito.barrio = request.POST['barrio']
            deposito.id_localidad = request.POST['id_localidad']
            deposito.id_encargado = request.POST['id_encargado']

            if(deposito.nombre == "" or deposito.id_encargado == '0' or deposito.id_encargado == 0):
                return Response('Debe completar los campos nombre y encargado, son obligatorios', status = status.HTTP_400_BAD_REQUEST)
            else:
                if not validar_nombre_deposito_update(deposito.nombre, pk):
                    return Response('El depósito cargado ya existe', status = status.HTTP_400_BAD_REQUEST)
                else:
                    if actualizar_deposito(deposito, pk):
                        return Response('Depósito actualizado correctamente', status = status.HTTP_200_OK)
                    else:
                        return Response('Error en los datos', status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response('No fue posible actualizar el depósito', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            
            if deposito.nombre == '' or deposito.id_encargado == 0 or deposito.id_encargado == '0':
                return Response('Debe completar los campos nombre y encargado, son obligatorios', status = status.HTTP_400_BAD_REQUEST)
            else:
                if validar_nombre_deposito_insert(deposito.nombre):
                    if alta_deposito(deposito):
                        return Response('Depósito creado correctamente', status = status.HTTP_201_CREATED)
                    else:
                        return Response('Error al insertar el depósito', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('El depósito cargado ya existe', status = status.HTTP_400_BAD_REQUEST)
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


# ---------- Gestion de artículos ---------- #
class Articulo(APIView):
    """
    Acá va el GET, POST, PUT, DELETE de la entidad
    """
    def get(self, request, pk):
        try:
            articulo = obtener_articulo(pk)

            response = ArticuloSerializer(articulo)

            return Response(response.data, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('No fue posible obtener el artículo', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):

        try:
            articulo = ArticuloDto()

            articulo.descripcion = request.POST['descripcion']
            articulo.precio_unitario = request.POST['precio_unitario']
            articulo.cantidad_medida = request.POST['cantidad_medida']

            if articulo.precio_unitario == '' or articulo.precio_unitario == 0 or articulo.precio_unitario == '0':
                return Response('El campo precio unitario es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            if articulo.cantidad_medida == '' or articulo.cantidad_medida == 0 or articulo.cantidad_medida == '0':
                return Response('El campo cantidad de medida es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            if articulo_repetido(articulo.nombre):
                return Response('El artículo cargado ya existe', status = status.HTTP_400_BAD_REQUEST)
            else:
                if actualizar_articulo(articulo, pk):
                        return Response('Artículo actualizado correctamente', status = status.HTTP_200_OK)
                else:
                    return Response('Error en los datos', status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response('No fue posible actualizar el artículo', status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            articulo = ArticuloDto()

            if request.POST['nombre'] == '':
                return Response('El campo nombre es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.nombre = request.POST['nombre']

            if request.POST['descripcion'] != '':
                articulo.descripcion = request.POST['descripcion']
            else:
                articulo.descripcion = None

            if request.POST['precio_unitario'] == '' or request.POST['precio_unitario'] == '0' or request.POST['precio_unitario'] == 0:
                return Response('El campo precio unitario es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.precio_unitario = request.POST['precio_unitario']

            if request.POST['id_marca'] == '0' or request.POST['id_marca'] == 0:
                return Response('El campo marca es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.id_marca = request.POST['id_marca']

            if request.POST['id_categoria'] == '0' or request.POST['id_categoria'] == 0:
                return Response('El campo categoría es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.id_categoria = request.POST['id_categoria']

            if request.POST['id_unidad_medida'] == '0' or request.POST['id_unidad_medida'] == 0:
                return Response('El campo unidad de medida es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.id_unidad_medida = request.POST['id_unidad_medida']

            if request.POST['cantidad_medida'] == '' or request.POST['cantidad_medida'] == '0' or request.POST['cantidad_medida'] == 0:
                return Response('El campo cantidad de medida es obligatorio', status = status.HTTP_400_BAD_REQUEST)
            articulo.cantidad_medida = request.POST['cantidad_medida']


            if articulo_repetido(articulo.nombre):
                return Response('El artículo cargado ya existe', status = status.HTTP_400_BAD_REQUEST)
            else:
                if alta_articulo(articulo):
                    return Response('Artículo creado exitosamente', status = status.HTTP_201_CREATED)
                else:
                    return Response('Error al insertar el artículo', status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response('No fue posible insertar el artículo', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        
        try:
            delete_articulo(pk)
        except:
            return Response('Server Error', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response('Artículo dado de baja exitosamente', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_articulos(request):
    try:
        articulos = obtener_articulos()

        response = ArticulosSerializer(articulos, many = True)
    except Exception as e:
        print(e)
        return Response('No fue posible obtener los artículos', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_marcas(request):
    try: 
        marcas = obtener_marcas()

        response = MarcasSerializer(marcas, many = True)
    except Exception as e:
        return Response('No fue posible obtener las marcas', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_categorias(request):
    try:
        categorias = obtener_categorias()
        
        response = CategoriasSerializer(categorias, many = True)
    except Exception as e:
        print(e)
        return Response('No fue posible obtener las categorías', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_unidades_medida(request):
    try:
        unidades_medida = obtener_unidades_medida()

        response = UnidadesMedidaSerializer(unidades_medida, many = True)
    except Exception as e:
        print(e)
        return Response('No fue posible obtener las unidades de medida', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status = status.HTTP_200_OK)


    # --------- Gestion de pedidos --------- #
class Pedido(APIView):
    """
    Acá va el GET, POST, PUT, DELETE de la entidad
    """
    def get(self, request, pk):
        try:
            pedido = obtener_pedido(pk)

            response = PedidoSerializer(pedido)

        except Exception as e:
            print(e)
            return Response('No fue posible obtener el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response.data, status = status.HTTP_200_OK)


    def put(self, request, pk):

        pass

    def post(self, request):
        
        pass

    def delete(self, request, pk):
        
        pass


@api_view(['GET'])
def get_pedidos(request):
    try:
        pedidos = obtener_pedidos(request.user)

        response = PedidosSerializer(pedidos, many = True)
    except Exception as e:
        print(e)
        return Response('No fue posible obtener los pedidos', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response.data, status = status.HTTP_200_OK)


@api_view(['POST'])
def pedido_confirmado(request, pk):
    try:
        response = _db.get_data_from_procedure(connection = connection,
                                                proc_name = 'sp_procesar_pedido_confirmado',
                                                proc_params = {
                                                    'id_pedido': pk,
                                                    'id_usuario': request.user.id
                                                })
    except Exception as e:
        print(e)
        return Response('No fue posible confirmar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response[0]['v_result'] == 'OK':
        return Response('Pedido confirmado exitosamente', status = status.HTTP_200_OK)
    else:
        return Response('No fue posible confirmar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pedido_modificado(request, pk):
    try:
        detalles_pedido = eval(request.data['detalles_pedido'])
        lst_detalles_pedido = armado_lista(pk, detalles_pedido)

        if not delete_detalles_pedido(pk):
            raise Exception('Error al eliminar los detalles del pedido')

        insert_detalles_pedido(lst_detalles_pedido)
    except Exception as e:
        print(e)
        return Response('No fue posible modificar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if request.data['observaciones'] != '':
            observaciones = request.data['observaciones']
        else:
            observaciones = ''

        response = _db.get_data_from_procedure(connection = connection,
                                                proc_name = 'sp_procesar_pedido_modificado',
                                                proc_params = {
                                                    'id_pedido': pk,
                                                    'id_usuario': request.user.id,
                                                    'observaciones': observaciones
                                                })
    
    except Exception as e:
        print(e)
        return Response('No fue posible confirmar el pedido modificado', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response[0]['v_result'] == 'OK':
        return Response('Pedido modificado exitosamente', status = status.HTTP_200_OK)
    else:
        return Response('No fue posible modificar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pedido_rechazado(request, pk):
    try:
        if request.POST['observaciones'] != '':
            observaciones = request.POST['observaciones']
        else:
            observaciones = ''

        response = _db.get_data_from_procedure(connection = connection,
                                                proc_name = 'sp_procesar_pedido_rechazado',
                                                proc_params = {
                                                    'id_pedido': pk,
                                                    'id_usuario': request.user.id,
                                                    'observaciones': observaciones
                                                })
    except Exception as e:
        print(e)
        return Response('No fue posible rechazar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response[0]['v_result'] == 'OK':
        return Response('Pedido rechazado exitosamente', status = status.HTTP_200_OK)
    else:
        return Response('No fue posible rechazar el pedido', status = status.HTTP_500_INTERNAL_SERVER_ERROR)

      
# ------------ Gestion Recepcion Traspaso ----------------
@api_view(['GET'])
def get_traspasos(request):
    try:
        traspasos = obtener_traspasos_al_deposito(request.user)

        response = TraspasosSerializer(traspasos, many=True)

        return Response(response.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)      
        return Response('No fué posible obtener los traspasos', status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
def get_traspaso(request, pk):
    try:
        response = obtener_traspaso(pk)


        # el controller me lo devuelve ya serializado (a mano), 
        # por eso no requiere serializarlo acá, ni hacer response.data
        if response is not None:
            
            return Response(response, status=status.HTTP_200_OK)
        else:
            raise Exception

    except Exception as e:
        print(e)      
        return Response('No fué posible obtener el traspaso', status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['POST'])
def procesar_traspaso_confirmado(request, pk):
    try:
        
        if traspaso_confirmado(pk, request.user.id):
            return Response('Registro exitoso', status=status.HTTP_200_OK)
        else:
            raise Exception

    except Exception as e:
        print(e)
        return Response('No fúe posible procesar traspaso', status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


@api_view(['POST'])
def procesar_traspaso_modificado(request, pk):
    try:

        traspaso = TraspasoDto()

        traspaso.id = pk
        traspaso.observaciones = request.data['observaciones']
        traspaso.detalle_traspaso = request.data['detalle_traspaso']

        if traspaso_modificado(request.user.id, traspaso):
            return Response('Registro exitoso', status=status.HTTP_200_OK)
        else:
            raise Exception

    except Exception as e:
        print(e)
        return Response('No fúe posible procesar traspaso', status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


@api_view(['POST'])
def procesar_traspaso_rechazado(request, pk):
    try:

        traspaso = TraspasoDto()

        traspaso.id = pk
        traspaso.observaciones = request.data['observaciones']

        if traspaso_rechazado(request.user.id, traspaso):
            return Response('Traspaso rechazado', status=status.HTTP_200_OK)
        else:
            raise Exception

    except Exception as e:
        print(e)
        return Response('No fúe posible procesar traspaso', status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

      
@api_view(['GET'])
def get_deposito_usuario(request):
    try:
        deposito = obtener_deposito_usuario(request.user)

        if deposito is not None:
            response = DepositosSerializerSmall(deposito, many=False)
        else:
            raise Exception
    except Exception as e:
        print(e)
        return Response('No fue posible obtener el depósito', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(response.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_existencias(request):
    try:
        response = obtener_existencias(request.user)

        # response = ExistenciasSerializer(existencias, many = True)
    
    except Exception as e:
        print(e)
        return Response('No fue posible obtener las existencias', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(response, status = status.HTTP_200_OK)


@api_view(['POST'])
def insert_traspaso(request):
    try:

        traspaso = TraspasoDtoInsert()

        traspaso.id_deposito_origen = request.data['id_deposito_origen']
        traspaso.id_deposito_destino = request.data['id_deposito_destino']
        traspaso.id_usuario_genero = request.user.id
        
        detalle_traspaso = None

        try:
            detalle_traspaso = eval(request.data['detalle_traspaso'])
        except:
            detalle_traspaso = request.data['detalle_traspaso']

        if alta_traspaso(traspaso, detalle_traspaso):
            return Response('Traspaso realizado con éxito', status = status.HTTP_200_OK)

    
    except Exception as e:
        print(e)
        return Response('No fue posible realizar el traspaso', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            




