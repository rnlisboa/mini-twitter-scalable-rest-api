from rest_framework import serializers

from posts.models import PostModel
from users.serializers.user_serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = PostModel
        fields = '__all__'

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['owner', 'text', 'status', 'image']
