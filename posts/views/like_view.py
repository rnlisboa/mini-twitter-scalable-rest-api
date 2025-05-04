from posts.models import LikeModel

from rest_framework.permissions    import IsAuthenticated
from rest_framework.decorators     import action
from rest_framework.response       import Response
from rest_framework                import (status, 
                                       viewsets)

from posts.serializers.like_serializer import LikeInputSerializer, LikeSerializer
from posts.use_cases.like_post         import LikePostUseCase
from posts.use_cases.unlike_post       import UnLikePostUseCase
from utils.decorators.serializer_validator import validate_serializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = LikeModel.objects.all()
    serializer_class = LikeSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @validate_serializer(LikeSerializer)
    def like_post(self, request, *args, **kwargs):
        try:
            use_case = LikePostUseCase()
            post_like_count = use_case.execute(
                user=request.validated_data['user'],
                post=request.validated_data['post']
            )        
            
            return Response(data={"post_like_count": post_like_count}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    @validate_serializer(LikeInputSerializer)
    def unlike_post(self, request, *args, **kwargs):
        try:
            use_case = UnLikePostUseCase()
            use_case.execute(
                user=request.validated_data['user'],
                post=request.validated_data['post']
            )        
        
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)