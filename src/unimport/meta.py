from typing import Dict

__all__ = ("MakeSingletonWithParams",)


class MakeSingletonWithParams(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        """Returns the same instance if args and kwargs are the same,
        otherwise, creates a new instance."""
        key = (cls, args, frozenset(kwargs.items()))
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]
