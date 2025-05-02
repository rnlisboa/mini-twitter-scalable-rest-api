from rest_framework import serializers
from users.models import FollowModel
from users.serializers.user_serializer import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following = UserSerializer()

    class Meta:
        model = FollowModel
        fields = ('id', 'user', 'following', 'created_at')