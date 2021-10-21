from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    # ---------- Gestión de usuarios ----------- #
    
    path('usuarios/', views.get_usuarios), # Obtener todos los usuarios, llega a través de un GET
    path('usuario/', views.Usuario.as_view()), # Alta de usuario, llega a través de POST
    path('usuario/<int:pk>/', views.Usuario.as_view()), # Consulta, Baja y Modificación de un usuario, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo
    
    path('tipos-rol/', views.get_tipos_rol), #Obtener todos los tipos_rol, llega a través de GET

    # ---------- Gestión de depósitos ---------- #

    path('deposito/', views.Deposito.as_view()), # Alta de depósito, llega a través de POST
    path('depositos/', views.get_depositos), # Obtener todos los depósitos, llega a través de un GET
    path('deposito/<int:pk>/', views.Deposito.as_view()), # Consulta, Baja y Modificación de un depósito, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo

    path('deposito/deposito_usuario/', views.get_deposito_usuario), # Get deposito del usuario. llega a traves de GET

    path('localidades/', views.get_localidades), #Obtener todas las localidades, llega a través de GET 
  
    path('encargados/', views.get_encargados), #Obtener todos los encargados, llega a través de GET


    # ---------- Gestión de artículos ---------- #
    path('articulos/', views.get_articulos), # Obtener todos los artículos, llega a través de un GET
    path('articulo/', views.Articulo.as_view()), #Alta de artículo, llega a través de POST
    path('articulo/<int:pk>/', views.Articulo.as_view()), # Consulta, Baja y Modificación de un artículo, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo

    path('marcas/', views.get_marcas), #Obtener todas las marcas, llega a través de GET

    path('categorias/', views.get_categorias), #Obtener todas las categorías, llega a través de GET

    path('unidades_medida/', views.get_unidades_medida), #Obtener todas las unidades de medida, llega a través de GET



    # --------- Gestión de pedidos --------- #
    path('pedidos/', views.get_pedidos), #Obtener todos los pedidos, llega a través de GET
    path('pedido/<int:pk>/', views.Pedido.as_view()), #Consulta de un pedido, llega a través de GET. El parámetro que se recibe en la URL es la pk del mismo

    path('pedido_confirmado/<int:pk>/', views.pedido_confirmado), #Confirma el pedido, llega a través de POST. El parámetro que se recibe en la URL es la pk del mismo
    path('pedido_modificado/<int:pk>/', views.pedido_modificado), #Modifica el pedido, llega a través de POST. El parámetro que se recibe en la URL es la pk del mismo
    path('pedido_rechazado/<int:pk>/', views.pedido_rechazado), #Rechaza el pedido, llega a través de POST. El parámetro que se recibe en la URL es la pk del mismo


    # ---------- Gestion de existencias ---------- #
    path('existencias/', views.get_existencias), #Obtener todas las existencias, llega a través de GET

  
    # ---------- Gestion de traspasos ---------- #
  
    # ---------- Generacion ---------- #
    path('traspaso/', views.insert_traspaso), #Alta de traspaso, llega a través de POST
  
    # --------- Recepcion ------- #
    path('traspasos/', views.get_traspasos), #Obtener todas los traspasos, llega a través de GET
    path('traspaso/<int:pk>/', views.get_traspaso), #Obtener un traspaso, llega a través de GET
    path('traspaso/procesar/confirmado/<int:pk>/', views.procesar_traspaso_confirmado), # Procesar un traspaso confirmado, llega a través de POST
    path('traspaso/procesar/modificado/<int:pk>/', views.procesar_traspaso_modificado), # Procesar un traspaso modificado, llega a través de POST
    path('traspaso/procesar/rechazado/<int:pk>/', views.procesar_traspaso_rechazado), # Procesar un traspaso rechazado, llega a través de POST


    # ---------- Gestion de reportes ---------- #
    path('reportes/cantidad_movimientos_depositos/', views.get_reporte_cantidad_movimientos_depositos),
]