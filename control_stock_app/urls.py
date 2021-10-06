from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    # ---------- Gestion de usuarios ----------- #
    
    path('usuarios/', views.get_usuarios), # Obtener todos los usuarios, llega a través de un POST
    path('usuario/', views.Usuario.as_view()), # Alta de usuario, llega a través de POST
    path('usuario/<int:pk>/', views.Usuario.as_view()), # Consulta, Baja y Modificación de un usuario, llega a través de GET, DELETE y PUT. El parámetro que se recibe en la URL es la pk del mismo

    # ---------------------------------------------- #
    
]