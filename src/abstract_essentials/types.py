"""
abstract_essentials.types
=========================
Primitive type checks and coercion helpers.
"""


def is_number(s):
    """Return True if *s* can be parsed as a float."""
    try:
        float(s)
        return True
    except Exception:
        return False


def make_list(obj, commaparse=True):
    """
    Coerce *obj* to a list.

    - A comma-containing string is split on commas (unless *commaparse* is False).
    - sets and tuples become lists.
    - lists are returned unchanged.
    - anything else is wrapped in a single-element list.
    """
    if isinstance(obj, str):
        if ',' in obj and commaparse is True:
            obj = obj.split(',')
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, list):
        return obj
    return [obj]


__all__ = ["is_number", "make_list"]
