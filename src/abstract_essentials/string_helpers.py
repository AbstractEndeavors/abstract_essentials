"""
abstract_essentials.string_helpers
===================================
String stripping helpers (eatAll and friends).
"""


def eatInner(string, list_objects):
    """Strip leading characters that appear in *list_objects*."""
    if not isinstance(list_objects, list):
        list_objects = [list_objects]
    if not isinstance(string, str):
        string = str(string)
    if string and list_objects:
        for char in string:
            if string:
                if char not in list_objects:
                    return string
                string = string[1:]
    return string


def eatOuter(string, list_objects):
    """Strip trailing characters that appear in *list_objects*."""
    if not isinstance(list_objects, list):
        list_objects = [list_objects]
    if not isinstance(string, str):
        string = str(string)
    if string and list_objects:
        for _ in range(len(string)):
            if string:
                if string[-1] not in list_objects:
                    return string
                string = string[:-1]
    return string


def eatAll(string, list_objects):
    """Strip both leading and trailing characters that appear in *list_objects*."""
    if not isinstance(list_objects, list):
        list_objects = [list_objects]
    if not isinstance(string, str):
        string = str(string)
    if string and list_objects:
        string = eatInner(string, list_objects)
    if string and list_objects:
        string = eatOuter(string, list_objects)
    return string


__all__ = ["eatInner", "eatOuter", "eatAll"]
