from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from users.serializer import UserSerializer
from users.services import UserService

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors,
                'message': "Houveram erros de validação."
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        password = request.data['password']
        try:
            UserService.create_user(
                username=data['username'],
                email=data['email'],
                password=password
            )
            return Response({'message': 'Usuário cadastrado com sucesso!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
