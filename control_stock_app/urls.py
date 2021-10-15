from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    # ---------- Gestion de usuarios ----------- #
    
    path('usuarios/', views.get_usuarios), # Obtener todos los usuarios, llega a través de un GET
    path('usuario/', views.Usuario.as_view()), # Alta de usuario, llega a través de POST
    path('usuario/<int:pk>/', views.Usuario.as_view()), # Consulta, Baja y Modificación de un usuario, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo
    
    path('tipos-rol/', views.get_tipos_rol), #Obtener todos los tipos_rol, llega a través de GET

    # ---------- Gestion de depósitos ---------- #

    path('deposito/', views.Deposito.as_view()), # Alta de depósito, llega a través de POST
    path('depositos/', views.get_depositos), # Obtener todos los depósitos, llega a través de un GET
    path('deposito/<int:pk>/', views.Deposito.as_view()), # Consulta, Baja y Modificación de un depósito, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo

    path('localidades/', views.get_localidades), #Obtener todas las localidades, llega a través de GET 
  
    path('encargados/', views.get_encargados), #Obtener todos los encargados, llega a través de GET


    # ---------- Gestion de artículos ---------- #
    path('articulos/', views.get_articulos), # Obtener todos los artículos, llega a través de un GET
    path('articulo/', views.Articulo.as_view()), #Alta de artículo, llega a través de POST
    path('articulo/<int:pk>/', views.Articulo.as_view()), # Consulta, Baja y Modificación de un artículo, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo

    path('marcas/', views.get_marcas), #Obtener todas las marcas, llega a través de GET

    path('categorias/', views.get_categorias), #Obtener todas las categorías, llega a través de GET

    path('unidades_medida/', views.get_unidades_medida), #Obtener todas las unidades de medida, llega a través de GET

    path('existencias/', views.get_existencias), #Obtener todas las existencias, llega a través de GET
]