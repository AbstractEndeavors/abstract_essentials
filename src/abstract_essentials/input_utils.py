"""
abstract_essentials.input_utils
==================================
Dataclass / annotated-class construction helpers.
"""


def get_inputs(cls, *args, **kwargs):
    """
    Dynamically construct a (data)class instance from *args*/*kwargs*,
    filling any missing values from the class's own defaults.
    """
    fields = list(cls.__annotations__.keys())
    values = {}

    args = list(args)
    for field in fields:
        if field in kwargs:
            values[field] = kwargs[field]
        elif args:
            values[field] = args.pop(0)
        else:
            values[field] = getattr(cls(), field)

    return cls(**values)


__all__ = ["get_inputs"]
