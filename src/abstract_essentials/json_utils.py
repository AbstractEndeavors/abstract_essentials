"""
abstract_essentials.json_utils
================================
JSON parsing, traversal, and serialisation helpers.
"""
import os
import re
import json
import logging

_json_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# low-level parse helpers
# ---------------------------------------------------------------------------

def try_json_loads(data):
    try:
        return json.loads(data)
    except Exception:
        return None


def safe_json_loads(data):
    if not isinstance(data, dict):
        data = try_json_loads(data) or data
    return data


def clean_invalid_newlines(json_string, line_replacement_value=''):
    """Remove bare newlines that fall outside double-quoted strings."""
    pattern = r'(?<!\\)\n(?!([^"]*"[^"]*")*[^"]*$)'
    return re.sub(pattern, line_replacement_value, json_string)


def read_malformed_json(json_string, line_replacement_value="*n"):
    """Attempt to parse a (possibly malformed) JSON string after cleaning it."""
    if isinstance(json_string, str):
        json_string = clean_invalid_newlines(
            json_string, line_replacement_value=line_replacement_value
        )
    return safe_json_loads(json_string)


# ---------------------------------------------------------------------------
# traversal
# ---------------------------------------------------------------------------

def get_value_from_path(json_data, path, line_replacement_value='*n*'):
    """Traverse nested JSON along *path* and return the value found."""
    current_data = safe_json_loads(json_data)
    for step in path:
        current_data = safe_json_loads(current_data[step])
        if isinstance(current_data, str):
            current_data = read_malformed_json(
                current_data, line_replacement_value=line_replacement_value
            )
    return current_data


def find_paths_to_key(json_data, key_to_find, line_replacement_value='*n*'):
    """Return every path (list of keys/indices) that leads to *key_to_find*."""
    def _search(data, current_path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    paths.append(new_path)
                if isinstance(value, str):
                    try:
                        nested = read_malformed_json(
                            value, line_replacement_value=line_replacement_value
                        )
                        _search(nested, new_path)
                    except json.JSONDecodeError:
                        pass
                _search(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                _search(item, current_path + [index])

    paths = []
    _search(json_data, [])
    return paths


def get_any_value(json_obj, key, line_replacement_value="*n*"):
    """
    Fetch the value(s) for *key* from a JSON object, JSON string, or JSON file path.
    """
    if isinstance(json_obj, str):
        if os.path.isfile(json_obj):
            with open(json_obj, 'r', encoding='UTF-8') as f:
                json_obj = f.read()
    json_data = read_malformed_json(json_obj)
    paths_to_value = find_paths_to_key(json_data, key)
    if not isinstance(paths_to_value, list):
        paths_to_value = [paths_to_value]
    for i, path_to_value in enumerate(paths_to_value):
        paths_to_value[i] = get_value_from_path(json_data, path_to_value)
        if isinstance(paths_to_value[i], str):
            paths_to_value[i] = paths_to_value[i].replace(line_replacement_value, '\n')
    if isinstance(paths_to_value, list):
        if len(paths_to_value) == 0:
            paths_to_value = None
        elif len(paths_to_value) == 1:
            paths_to_value = paths_to_value[0]
    return paths_to_value


def flatten_json(data, parent_key='', sep='_'):
    """
    Flatten a nested JSON object into a single dict.

    Keys encode the nesting path using *sep* as a separator.
    """
    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(flatten_json(value, new_key, sep=sep).items())
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    items.extend(flatten_json(item, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, value))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            items.extend(flatten_json(item, f"{parent_key}{sep}{i}", sep=sep).items())
    else:
        items.append((parent_key, data))
    return dict(items)


# ---------------------------------------------------------------------------
# file-level JSON I/O
# ---------------------------------------------------------------------------

def _write_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as fh:
        fh.write(str(data))


def _write_json(data, file_path, ensure_ascii=False, indent=4):
    with open(file_path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=ensure_ascii, indent=indent)


def _safe_write_json(data, file_path, ensure_ascii=False, indent=4):
    if isinstance(data, (dict, list, tuple)):
        _write_json(data, file_path, ensure_ascii=ensure_ascii, indent=indent)
    else:
        _write_file(data, file_path)


def _read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def _output_read_write_error(e, function_name, file_path,
                              valid_file_path=None, data=None, is_read=False):
    msg = f"Error in {function_name}; {e}\nFile path: {file_path} "
    if valid_file_path is None:
        msg += f"\nValid File path: {valid_file_path} "
    if not is_read:
        msg += f"\nData: {data} "
    _json_logger.error(msg)


def validate_file_path(file_path, is_read=False):
    if file_path and isinstance(file_path, str):
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            return file_path
        if not is_read:
            dirname = os.path.dirname(file_path)
            if os.path.isdir(dirname):
                return file_path
    return None


def get_file_path(*args, is_read=False, **kwargs):
    for file_path in list(args):
        if validate_file_path(file_path, is_read=is_read):
            return file_path
    for file_path in list(kwargs.values()):
        if validate_file_path(file_path, is_read=is_read):
            return file_path
    return None


def safe_dump_to_file(data, file_path=None, ensure_ascii=False, indent=4, *args, **kwargs):
    """Serialise *data* to *file_path* (JSON for dict/list/tuple, else text)."""
    is_read = False
    file_args = [file_path, data]
    valid_file_path = get_file_path(*file_args, *args, is_read=is_read, **kwargs)

    if valid_file_path:
        file_path = valid_file_path
        if file_path == file_args[-1]:
            data = file_args[0]
    if file_path is not None and data is not None:
        try:
            _safe_write_json(data, file_path, ensure_ascii=ensure_ascii, indent=indent)
        except Exception as e:
            _output_read_write_error(
                e, 'safe_dump_to_file', file_path, valid_file_path, is_read=is_read
            )
    else:
        _json_logger.error("file_path and data must be provided to safe_dump_to_file")


def safe_read_from_json(file_path, *args, **kwargs):
    """Read and return JSON content from *file_path* (None on failure)."""
    is_read = True
    valid_file_path = get_file_path(file_path, *args, is_read=is_read, **kwargs)
    if valid_file_path:
        file_path = valid_file_path
    try:
        return _read_json(file_path)
    except Exception as e:
        _output_read_write_error(
            e, 'safe_read_from_json', file_path, valid_file_path, is_read=is_read
        )
        return None


def safe_load_from_json(*args, **kwargs):
    """Alias for :func:`safe_read_from_json`."""
    return safe_read_from_json(*args, **kwargs)


def safe_dump_to_json(*args, **kwargs):
    """Alias for :func:`safe_dump_to_file`."""
    return safe_dump_to_file(*args, **kwargs)


def dump_if_json(obj):
    if isinstance(obj, dict):
        return json.dumps(obj)
    return obj

def find_keys(data, target_keys):
    def _find_keys_recursive(data, target_keys, values):
        if isinstance(data, dict):
            for key, value in data.items():
                if key in target_keys:
                    values.append(value)
                _find_keys_recursive(value, target_keys, values)
        elif isinstance(data, list):
            for item in data:
                _find_keys_recursive(item, target_keys, values)
    
    values = []
    _find_keys_recursive(data, target_keys, values)
    return values

__all__ = [
    "try_json_loads", "safe_json_loads", "clean_invalid_newlines",
    "read_malformed_json", "get_value_from_path", "find_paths_to_key",
    "get_any_value", "flatten_json", "safe_dump_to_file", "safe_read_from_json",
    "safe_load_from_json", "safe_dump_to_json", "dump_if_json",
    "validate_file_path", "get_file_path","find_keys"
]
