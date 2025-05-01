from users.models import FollowModel

from rest_framework.decorators import action
from rest_framework.response   import Response
from rest_framework            import (status, 
                                       viewsets)

from users.serializer import FollowSerializer
from users.use_cases.follow_use_case.follow_user import FollowUserUseCase
from users.use_cases.follow_use_case.get_following_users import GetFollowingUserUseCase
from users.use_cases.follow_use_case.unfollow_user import UnfollowUserUseCase

class FollowViewSet(viewsets.ModelViewSet):
    queryset = FollowModel.objects.all()

    serializer_class = FollowSerializer
    
    @action(detail=False, methods=['POST'])
    def follow_user(self, *args, **kwargs):
        req = self.request.data

        user_id = req['user_id'] if 'user_id' in req else None
        follower_id = req['follower_id'] if 'follower_id' in req else None

        try:
            use_case = FollowUserUseCase()
            use_case.execute(user_id=user_id, follower_id=follower_id)
            return Response({'message': 'Novo seguidor adicionado!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE'])
    def unfollow_user(self, *args, **kwargs):
        req = self.request.data

        user_id = req['user_id'] if 'user_id' in req else None
        follower_id = req['follower_id'] if 'follower_id' in req else None
        try:
            use_case = UnfollowUserUseCase()
            use_case.execute(user_id=user_id, follower_id=follower_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    def get_follow_user(self, *args, **kwargs):
        req = self.request.query_params

        user_id = req['user_id'] if 'user_id' in req else None

        if not user_id:
            return Response({'error': 'Id do usuário não enviado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = GetFollowingUserUseCase()
            followers = use_case.execute(user_id=user_id)
            serializer = self.serializer_class(followers, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
