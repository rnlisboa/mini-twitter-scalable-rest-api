from functools import wraps
from rest_framework.response import Response
from rest_framework          import status

def validate_serializer(serializer_class):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'errors': serializer.errors,
                    'message': 'Houveram erros de validação.'
                }, status=status.HTTP_400_BAD_REQUEST)
            request.validated_data = serializer.validated_data
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator
