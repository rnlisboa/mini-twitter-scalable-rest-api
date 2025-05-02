from posts.models import LikeModel

from rest_framework.permissions    import IsAuthenticated
from rest_framework.decorators     import action
from rest_framework.response       import Response
from rest_framework                import (status, 
                                       viewsets)

from posts.serializers.like_serializer import LikeSerializer
from posts.use_cases.like_post         import LikePostUseCase
from posts.use_cases.unlike_post       import UnLikePostUseCase
from utils.decorators.serializer_validator import validate_serializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @validate_serializer(LikeSerializer)
    def like_post(self, *args, **kwargs):
        try:
            use_case = LikePostUseCase()
            post = use_case.execute(
                user=serializer.validated_data['user'],
                post=serializer.validated_data['post']
            )        
            serializer = self.serializer_class(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    @validate_serializer(LikeSerializer)
    def unlike_post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        try:
            use_case = UnLikePostUseCase()
            use_case.execute(
                user=serializer.validated_data['user'],
                post=serializer.validated_data['post']
            )        
        
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)