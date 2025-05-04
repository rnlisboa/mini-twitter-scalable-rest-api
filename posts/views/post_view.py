from posts.models import PostModel

from django.core.cache import cache

from rest_framework.permissions    import IsAuthenticated
from rest_framework.pagination     import PageNumberPagination
from rest_framework.decorators     import action
from rest_framework.response       import Response
from rest_framework                import (status,
                                       viewsets)


from posts.serializers.post_serializer import CreatePostSerializer, PostSerializer
from posts.use_cases.get_following_post import GetFollowingPostUseCase
from posts.use_cases.register_post import RegisterPostUseCase
from utils.decorators.param_validator import validate_required_params
from utils.decorators.serializer_validator import validate_serializer

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @validate_serializer(CreatePostSerializer)
    def register_post(self, request, *args, **kwargs):
        try:
            use_case = RegisterPostUseCase()

            post = use_case.execute(
                owner=request.validated_data['owner'], 
                text=request.validated_data['text'], 
                status=request.validated_data['status'], 
                image=request.validated_data['image']
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
        page = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('page_size', Pagination.page_size)

        cache_key = f"user_feed:{user_id}:page:{page}:size:{page_size}"
        if page == '1':
            cached_feed = cache.get(cache_key)
            if cached_feed:
                return Response(data=cached_feed, status=status.HTTP_200_OK)
        
        try:
            use_case = GetFollowingPostUseCase()
            posts = use_case.execute(user_id=user_id)            
            
            serializer = self.serializer_class(posts, many=True)
            paginator = Pagination()
            paginated_posts = paginator.paginate_queryset(posts, self.request)
            serializer = self.serializer_class(paginated_posts, many=True)

            if page == '1':
                cache.set(cache_key, serializer.data, timeout=60 * 5)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
