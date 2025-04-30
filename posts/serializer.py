from rest_framework import serializers

from posts.models import PostModel
from users.serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PostModel
        fields = '__all__'