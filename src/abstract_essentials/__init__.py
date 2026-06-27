"""
abstract_essentials
====================
Standalone, stdlib-only utility library.

All public symbols are re-exported here so existing call-sites that do::

    from abstract_essentials import get_any_value, lazy_import, ...

continue to work without change.
"""

from .types import (
    is_number,
    make_list,
)

from .string_helpers import (
    eatInner,
    eatOuter,
    eatAll,
)

from .utils import (
    is_file,
    is_dir,
    join_path,
    get_safe_basename,
    get_safe_dirname,
    get_safe_splitext,
    get_file_parts,
    get_home_dir,
    safe_join,
    raw_create_dirs,
    makedirs,
    get_directory,
    get_dirlist,
    get_files,
    get_files_and_dirs,
)

from .read_write_utils import (
    write_to_file,
    read_from_file,
)

from .json_utils import (
    try_json_loads,
    safe_json_loads,
    clean_invalid_newlines,
    read_malformed_json,
    get_value_from_path,
    find_paths_to_key,
    get_any_value,
    flatten_json,
    safe_dump_to_file,
    safe_read_from_json,
    safe_load_from_json,
    safe_dump_to_json,
    dump_if_json,
    validate_file_path,
    get_file_path,
    find_keys
)

from .mime_utils import (
    MIME_TYPES,
    MEDIA_TYPES,
    derive_media_type,
    get_mime_type,
    make_key_map,
)

from .caller_utils import (
    get_caller,
    get_caller_path,
    get_caller_dir,
)

from .env_utils import (
    get_env_value,
)

from .input_utils import (
    get_inputs,
)

from .lazy_utils import (
    nullProxy,
    lazy_import,
    lazy_import_single,
    get_lazy_attr,
    lazy_module,
)

from .log_utils import (
    LevelFilter,
    SafeFormatter,
    get_logFile,
    LOG_FORMAT,
    DATE_FORMAT,
    LOG_ROOT,
)

from .singleton_utils import (
    SingletonMeta,
)

from .url_utils import (
    parse_url,
)

from .list_utils import (
    get_sort,
    combineList,
    find_original_case,
    ensure_nested_list,
    make_list_add,
    recursive_json_list,
    filter_json_list_values,
    get_highest_value_obj,
    safe_list_return,
    get_actual_number,
    compare_lists,
    remove_from_list,
    list_set,
    get_symetric_difference,
    make_list_it,
    get_single_from_list,
    get_keys,
    get_only_kwargs,
    get_desired_key_values,
    makeParams,
    prune_inputs,
    run_pruned_func,
)
from .file_utils import (
    mkdirs, makedirs, raw_create_dirs,
    safe_join,
    get_home_folder,
    get_current_path,get_slash,
    get_ext,split_text,
    get_base_name,
    sanitize_filename,
    get_abs_name_of_this,
    get_file_name
    )

# stdlib re-exports (back-compat for consumers that do
# ``from abstract_essentials import os, json, socket, ...``)
import os       # noqa: F401  (re-exported intentionally)
import sys      # noqa: F401
import json     # noqa: F401
import socket   # noqa: F401
import logging  # noqa: F401

__all__ = [
    # types
    "is_number", "make_list",
    # string_helpers
    "eatInner", "eatOuter", "eatAll",
    # utils (path / fs)
    "is_file", "is_dir", "join_path",
    "get_safe_basename", "get_safe_dirname", "get_safe_splitext",
    "get_file_parts", "get_home_dir",
    "safe_join", "raw_create_dirs", "makedirs", "get_directory",
    "get_dirlist", "get_files", "get_files_and_dirs",
    # read_write_utils
    "write_to_file", "read_from_file",
    # json_utils
    "try_json_loads", "safe_json_loads", "clean_invalid_newlines",
    "read_malformed_json", "get_value_from_path", "find_paths_to_key",
    "get_any_value", "flatten_json", "safe_dump_to_file",
    "safe_read_from_json", "safe_load_from_json", "safe_dump_to_json",
    "dump_if_json", "validate_file_path", "get_file_path",
    # mime_utils
    "MIME_TYPES", "MEDIA_TYPES", "derive_media_type", "get_mime_type", "make_key_map",
    # caller_utils
    "get_caller", "get_caller_path", "get_caller_dir",
    # env_utils
    "get_env_value",
    # input_utils
    "get_inputs",
    # lazy_utils
    "nullProxy", "lazy_import", "lazy_import_single", "get_lazy_attr", "lazy_module",
    # log_utils
    "LevelFilter", "SafeFormatter", "get_logFile",
    "LOG_FORMAT", "DATE_FORMAT", "LOG_ROOT",
    # singleton_utils
    "SingletonMeta",
    # url_utils
    "parse_url",
    # list_utils
    "get_sort", "combineList", "find_original_case", "ensure_nested_list",
    "make_list_add", "recursive_json_list", "filter_json_list_values",
    "get_highest_value_obj", "safe_list_return", "get_actual_number",
    "compare_lists", "remove_from_list", "list_set", "get_symetric_difference",
    "make_list_it", "get_single_from_list", "get_keys",
    "get_only_kwargs", "get_desired_key_values", "makeParams",
    "prune_inputs", "run_pruned_func",
    # stdlib re-exports
    "os", "sys", "json", "socket", "logging",
    "mkdirs", "makedirs", "raw_create_dirs",
    "safe_join",
    "find_keys",
    "get_home_folder",
    "get_current_path","get_slash",
    "get_ext","split_text",
    "get_base_name",
    "sanitize_filename",
    "get_abs_name_of_this",
    "get_file_name",
]
