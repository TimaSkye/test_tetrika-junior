from functools import wraps
import inspect


def strict(func):
    """Проверяет соответствие типов аргументов аннотациям функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        annotations = func.__annotations__
        for name, value in bound.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be {expected_type.__name__}, got {type(value).__name__}"
                    )
        return func(*args, **kwargs)

    return wrapper
