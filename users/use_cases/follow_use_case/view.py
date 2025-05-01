from users.models import FollowModel

from rest_framework.decorators import action
from rest_framework.response   import Response
from rest_framework            import (status, 
                                       viewsets)

from users.serializer import FollowSerializer
from users.use_cases.follow_use_case.follow_user import FollowUserUseCase
from users.use_cases.follow_use_case.get_following_users import GetFollowingUserUseCase
from users.use_cases.follow_use_case.unfollow_user import UnfollowUserUseCase

from utils.decorators.param_validator import validate_required_params

class FollowViewSet(viewsets.ModelViewSet):
    queryset = FollowModel.objects.all()

    serializer_class = FollowSerializer
    
    @action(detail=False, methods=['POST'])
    @validate_required_params(params=["user_id", "follower_id"], source="query_params")
    def follow_user(self, *args, **kwargs):
        req = self.request.data

        user_id = req['user_id']
        follower_id = req['follower_id']
        
        try:
            use_case = FollowUserUseCase()
            use_case.execute(user_id=user_id, follower_id=follower_id)
            return Response({'message': 'Novo seguidor adicionado!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE'])
    @validate_required_params(params=["user_id", "following_id"], source="query_params")
    def unfollow_user(self, *args, **kwargs):
        req = self.request.data
        user_id = req['user_id']
        follower_id = req['follower_id']

        try:
            use_case = UnfollowUserUseCase()
            use_case.execute(user_id=user_id, follower_id=follower_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    @validate_required_params(params=["user_id"], source="query_params")
    def get_follow_user(self, *args, **kwargs):
        user_id = self.request.query_params['user_id']

        try:
            use_case = GetFollowingUserUseCase()
            followers = use_case.execute(user_id=user_id)
            serializer = self.serializer_class(followers, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
