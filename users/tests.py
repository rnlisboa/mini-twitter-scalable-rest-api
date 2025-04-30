from django.test import TestCase, RequestFactory
from rest_framework import status
from .views import *
from . models import *
from django.contrib.auth.models import User

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = UserViewSet.as_view({'post': 'create_user'})

    def test_create_user_success(self):
        request_data = {
            'username': 'usertest',
            'email': 'user@teste.com',
            'password': 'password123'
        }
        request = self.factory.post('/users/create_user', request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'usertest')
        self.assertEqual(user.email, 'user@teste.com')

    def test_create_user_validation_error(self):
            request_data = {
                'username': 'usertest',
                'email': 'email invalido',
                'password': 'password123'
            }
            request = self.factory.post('/users/create_user', request_data)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(User.objects.count(), 0)
            print(response.data)
            self.assertEqual(
                response.data,
                {
                "errors": {
                    "email": [
                        "Insira um endereço de email válido."
                    ]
                },
                "message": "Houveram erros de validação."
            }
            )