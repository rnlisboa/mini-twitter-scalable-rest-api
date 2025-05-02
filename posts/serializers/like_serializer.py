from rest_framework import serializers

from posts.models import LikeModel

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeModel
        fields = '__all__'