from posts.models import PostModel

from rest_framework.permissions    import IsAuthenticated
from rest_framework.decorators     import action
from rest_framework.response       import Response
from rest_framework                import (status, 
                                       viewsets)


from posts.serializers.post_serializer import PostSerializer
from posts.use_cases.get_following_post import GetFollowingPostUseCase
from posts.use_cases.register_post import RegisterPostUseCase
from utils.decorators.param_validator import validate_required_params
from utils.decorators.serializer_validator import validate_serializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @validate_serializer(PostSerializer)
    def register_post(self, *args, **kwargs):
        try:
            use_case = RegisterPostUseCase()

            post = use_case.execute(
                owner=serializer.validated_data['owner'], 
                text=serializer.validated_data['text'], 
                status=serializer.validated_data['status'], 
                image=serializer.validated_data['image']
                )
            
            serializer = self.serializer_class(post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={
                "message": "Erro ao publicar",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @validate_required_params(params=["user_id"], source="query_params")
    def get_following_posts(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')

        try:
            use_case = GetFollowingPostUseCase()
            posts = use_case.execute(user_id=user_id)        

            serializer = self.serializer_class(posts, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
