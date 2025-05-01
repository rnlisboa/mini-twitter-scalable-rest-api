from django.core.exceptions import ObjectDoesNotExist
from functools import wraps


def get_object_or_error(model, **kwargs):
    """
    Função para obter um objeto ou lançar erro padronizado.
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise ValueError(f"{model.__name__} não encontrado.")


def handle_not_found(message="Objeto não encontrado."):
    """
    Decorador para capturar ObjectDoesNotExist e lançar ValueError com mensagem personalizada.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ObjectDoesNotExist:
                raise ValueError(message)
        return wrapper
    return decorator
