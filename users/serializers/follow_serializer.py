from rest_framework import serializers
from users.models import FollowModel
from users.serializers.user_serializer import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    following = UserSerializer()

    class Meta:
        model = FollowModel
        fields = ('id', 'following', 'created_at')