from django.contrib.auth.models import User

from users.serializers.user_serializer import UserSerializer
from rest_framework.decorators         import action
from rest_framework.response           import Response
from rest_framework                    import (status, 
                                        viewsets)

from users.use_cases.user_use_case.get_user_by_username import GetUserByUsernameUseCase
from users.use_cases.user_use_case.get_all_users        import GetAllUsersUseCase
from users.use_cases.user_use_case.register_user        import RegisterUserUseCase

from utils.decorators.param_validator import validate_required_params
from utils.decorators.serializer_validator import validate_serializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    @validate_serializer(UserSerializer)
    def register_user(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = RegisterUserUseCase()
            use_case.execute(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=self.request.data['password']
            )
            return Response({'message': 'Usuário cadastrado com sucesso!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    @validate_required_params(params=["username"], source="query_params")
    def get_user_by_username(self, *args, **kwargs):
        username = self.request.query_params['username']

        try:
            use_case = GetUserByUsernameUseCase()
            user = use_case.execute(username=username)
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'])
    def get_all_users(self, *args, **kwargs):
        try:
            use_case = GetAllUsersUseCase()
            users = use_case.execute()
            serializer = self.serializer_class(users)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)