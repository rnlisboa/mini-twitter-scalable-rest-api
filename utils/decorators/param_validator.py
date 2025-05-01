from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def validate_required_params(params: list[str], source: str = "query_params"):
    """
    Decorador para validar se os parâmetros obrigatórios estão presentes na requisição.

    :param params: Lista de campos obrigatórios a validar.
    :param source: 'query_params' (GET), 'data' (POST), ou 'request' (busca nos dois).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if source == 'query_params':
                data = request.query_params
            elif source == 'data':
                data = request.data
            else:
                data = request.query_params.copy()
                data.update(request.data)

            missing = [param for param in params if param not in data or not data.get(param)]

            if missing:
                return Response({
                    "error": f"Os seguintes campos são obrigatórios e não foram enviados: {', '.join(missing)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
