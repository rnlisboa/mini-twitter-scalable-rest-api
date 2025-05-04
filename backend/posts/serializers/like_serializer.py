from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import LikeModel, PostModel

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = '__all__'

class LikeInputSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=PostModel.objects.all())