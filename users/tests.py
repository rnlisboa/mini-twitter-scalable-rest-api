from django.test import TestCase, RequestFactory
from rest_framework import status

from users.views.follow_view import FollowViewSet
from users.views.user_view import UserViewSet
from . models import *
from django.contrib.auth.models import User

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = UserViewSet.as_view({'post': 'register_user'})
        self.follow_view = FollowViewSet.as_view({'post': 'follow_user'})
        self.unfolow_view =FollowViewSet.as_view({'delete': 'unfollow_user'})

    def test_register_user_success(self):
        request_data = {
            'username': 'usertest',
            'email': 'user@teste.com',
            'password': 'password123'
        }
        request = self.factory.post('/users/register_user', request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'usertest')
        self.assertEqual(user.email, 'user@teste.com')

    def test_register_user_validation_error(self):
            request_data = {
                'username': 'usertest',
                'email': 'email invalido',
                'password': 'password123'
            }
            request = self.factory.post('/users/register_user', request_data)
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
    
    def test_follow_user_success(self):
        user = User.objects.create_user(username='user1', email='user1@gmail.com', password='pass123')
        follower = User.objects.create_user(username='user2', email='user2@gmail.com', password='pass456')

        data = {
            'user_id': user.id,
            'follower_id': follower.id
        }
      
        request = self.factory.post('/users/follow/follow_user/', data)
        response = self.follow_view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FollowModel.objects.count(), 1)
        follow = FollowModel.objects.first()
        self.assertEqual(follow.user, user)
        self.assertEqual(follow.following, follower)
    
    def test_follow_user_already_following(self):
        user = User.objects.create_user(username='user1', email='user1@gmail.com', password='pass123')
        follower = User.objects.create_user(username='user2', email='user2@gmail.com', password='pass456')

        FollowModel.objects.create(user=user, following=follower)
   
        data = {
            'user_id': user.id,
            'follower_id': follower.id
        }
        request = self.factory.post('/users/follow/follow_user/', data)
        response = self.follow_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_unfollow_user_success(self):
        user = User.objects.create_user(username='user1', email='user1@gmail.com', password='pass123')
        follower = User.objects.create_user(username='user2', email='user2@gmail.com', password='pass456')

        FollowModel.objects.create(user=user, following=follower)
        data = {
            'user_id': user.id,
            'follower_id': follower.id,
        }
        request = self.factory.delete(
            '/users/follow/unfollow_user/', 
            data,
            content_type='application/json')
        response = self.unfolow_view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FollowModel.objects.count(), 0)