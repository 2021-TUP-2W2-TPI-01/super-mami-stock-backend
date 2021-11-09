import unittest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

class UsuariosTest(unittest.TestCase):

    def test_get_usuario(self):

        token = Token.objects.get(user__username='mramirez')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = client.get('/api/usuario/35/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)


    def test_get_usuarios(self):
        token = Token.objects.get(user__username='mramirez')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = client.get('/api/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)


    def test_get_usuarios_no_authentication(self):

        client = APIClient()    
        
        response = client.get('/api/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
