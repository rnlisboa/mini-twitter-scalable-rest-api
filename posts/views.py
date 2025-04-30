from django.shortcuts import render

from rest_framework.response                    import Response
from rest_framework.decorators                  import action
from rest_framework                             import status, viewsets
from rest_framework.permissions                 import IsAuthenticated
from rest_framework.pagination                  import PageNumberPagination
from rest_framework_simplejwt.authentication    import JWTAuthentication
from django.contrib.auth.models                 import User
from django.db.models                           import Q

from posts.serializer import PostSerializer
from .models                                    import *


class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer