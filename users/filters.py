from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from . import models as m


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')      
    email = filters.CharFilter(lookup_expr='icontains')      

    class Meta:
        model = User
        fields = ['id', 'username', 'email']