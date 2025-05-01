from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework.response   import Response
from users.serializer          import UserSerializer
from rest_framework            import (status, 
                                       viewsets)

from users.use_cases.user_use_case.get_user_by_username import GetUserByUsernameUseCase
from users.use_cases.user_use_case.get_user_by_email import GetUserByEmailUseCase
from users.use_cases.user_use_case.get_user_by_id       import GetUserByIdUseCase
from users.use_cases.user_use_case.get_all_users        import GetAllUsersUseCase
from users.use_cases.user_use_case.register_user         import RegisterUserUseCase

from utils.decorators.param_validator import validate_required_params

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register_user(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors,
                'message': "Houveram erros de validação."
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
    @validate_required_params(params=["user_id"], source="query_params")
    def get_user_by_id(self, *args, **kwargs):
        user_id = self.request.query_params['user_id']

        try:
            use_case = GetUserByIdUseCase()
            user = use_case.execute(user_id=user_id)
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
    
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
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'])
    @validate_required_params(params=["email"], source="query_params")
    def get_user_by_email(self, *args, **kwargs):
        email = self.request.query_params['email']

        try:
            use_case = GetUserByEmailUseCase()
            user = use_case.execute(email=email)
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'])
    def get_all_users(self, *args, **kwargs):
        try:
            use_case = GetAllUsersUseCase()
            users = use_case.execute()
            serializer = self.serializer_class(users)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)