from rest_framework import serializers
from django.contrib.auth.models import User

from users.models import FollowModel

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following = UserSerializer()

    class Meta:
        model = FollowModel
        fields = ('id', 'user', 'following', 'created_at')