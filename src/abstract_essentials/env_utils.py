"""
abstract_essentials.env_utils
================================
Standalone .env file reader.  No abstractEnv class dependency.
"""
import os

from .string_helpers import eatAll, eatOuter


def _split_eq(line):
    """Split a ``KEY=VALUE`` line into a cleaned ``[key, value]`` pair."""
    if '=' in line:
        key_side = line.split('=')[0]
        value_side = line[len(key_side + '='):]
        return [
            eatOuter(key_side, [' ', '', '\t']),
            eatAll(value_side, [' ', '', '\t', '\n']),
        ]
    return [line, None]


def _search_for_env_key(key, path, deep_scan=False):
    """Return the value for *key* within the env file at *path* (or None)."""
    highest = [None, 0]
    if path and os.path.isfile(path):
        with open(path, "r") as f:
            for line in f:
                line_key, line_value = _split_eq(line)
                if line_key == key:
                    return line_value
                if deep_scan and key:
                    key_parts = 0
                    for key_part in key.split('_'):
                        if key_part and key_part in line_key:
                            key_parts += len(key_part)
                    if float(key_parts / len(key)) >= 0.5 and key_parts > highest[1]:
                        highest = [line_value, key_parts]
                        return line_value
    return None


def get_env_value(key=None, path=None, file_name=None, deep_scan=False):
    """
    Retrieve the value of an environment variable from a .env-style file.

    Search order: supplied *path*, cwd, home dir, ``~/.envy_all``.

    Args:
        key:        variable name to look up (defaults to ``MY_PASSWORD``).
        path:       a directory to search, or a direct path to an env file.
        file_name:  env file name (defaults to ``.env``).
        deep_scan:  when True, fall back to fuzzy key matching.
    """
    key = key or 'MY_PASSWORD'
    file_name = file_name or '.env'
    current_folder = os.getcwd()

    if path and os.path.isfile(path):
        file_name = os.path.basename(path)
        path = os.path.dirname(path)
    else:
        path = path or current_folder

    home_folder = os.path.expanduser("~")
    envy_all = os.path.join(home_folder, '.envy_all')

    directories = []
    for directory in [path, current_folder, home_folder, envy_all]:
        if directory and os.path.isdir(directory) and directory not in directories:
            directories.append(directory)

    for directory in directories:
        env_path = os.path.join(directory, file_name)
        if os.path.isfile(env_path):
            value = _search_for_env_key(key=key, path=env_path, deep_scan=deep_scan)
            if value:
                return value
    return None


__all__ = ["get_env_value"]
