"""
abstract_essentials.caller_utils
==================================
Stack-inspection helpers for discovering the calling file's path/directory.
"""
import os
import inspect


def get_caller(i=None):
    """Return the filename of the calling frame *i* levels up (default 1)."""
    depth = 1 if i is None else int(i)
    stack = inspect.stack()
    if depth >= len(stack):
        depth = len(stack) - 1
    return stack[depth].filename


def get_caller_path(i=None):
    """Return the absolute, real path of the caller's file."""
    depth = 1 if i is None else int(i)
    file_path = get_caller(depth + 1)
    return os.path.realpath(file_path)


def get_caller_dir(i=None):
    """Return the absolute directory of the caller's file."""
    depth = 1 if i is None else int(i)
    abspath = get_caller_path(depth + 1)
    return os.path.dirname(abspath)


__all__ = ["get_caller", "get_caller_path", "get_caller_dir"]
