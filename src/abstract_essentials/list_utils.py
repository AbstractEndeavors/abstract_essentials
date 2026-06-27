"""
abstract_essentials.list_utils
================================
List and collection manipulation helpers.
"""
import inspect

from .types import make_list


def get_sort(ls: list, k: int = 0):
    ls.sort()
    return ls[k]


def combineList(ls: list, ls_n: list) -> list:
    for item in ls_n:
        ls.append(item)
    return ls


def find_original_case(input_list, search_string):
    for obj in input_list:
        if obj.lower() == search_string.lower():
            return obj
    return None


def ensure_nested_list(obj):
    if not isinstance(obj, list):
        return [obj]
    for element in obj:
        if not isinstance(element, list):
            return [obj]
    return obj


def make_list_add(obj, values):
    obj = list(obj)
    for each in list(values):
        obj.append(each)
    return obj


def recursive_json_list(json_list: dict, desired_values: dict) -> list:
    recursed_list = []
    for json_obj in json_list:
        bool_count = 0
        for desired_key, desired_value in desired_values.items():
            if desired_key in json_obj:
                if json_obj[desired_key] == desired_value:
                    bool_count += 1
        if bool_count == len(list(desired_values.keys())):
            recursed_list.append(json_obj)
    return recursed_list


def filter_json_list_values(json_list: list, keys: list):
    all_keys = {}
    for key in keys:
        unique_values = []
        for json_obj in json_list:
            if key in json_obj:
                if json_obj[key] not in unique_values:
                    unique_values.append(json_obj[key])
        all_keys[key] = unique_values
    return all_keys


def get_highest_value_obj(obj_list, function):
    return max(obj_list, key=function)


def safe_list_return(current_list, list_num=0):
    if len(current_list) >= list_num + 1:
        return current_list[int(list_num)]
    return None


def get_actual_number(reference_object, number_value):
    try:
        reference_length = len(reference_object)
    except Exception:
        reference_length = 0
    if reference_length == 0:
        return None
    return max(0, min(number_value, reference_length - 1))


def compare_lists(list_1, list_2):
    if len(list_1) > len(list_2):
        return False
    for each in list_1:
        if each not in list_2:
            return False
    return True


def remove_from_list(list_obj, key, value):
    return [obj for obj in list_obj if not (isinstance(obj, dict) and obj.get(key) == value)]


def list_set(obj):
    try:
        obj = list(set(obj))
    except Exception as e:
        print(f"{e}")
    return obj


def get_symetric_difference(obj_1, obj_2):
    set1 = set(obj_1)
    set2 = set(obj_2)
    return list(set1.symmetric_difference(set2))


def make_list_it(obj=None):
    return make_list(obj or [])


def get_single_from_list(list_obj, default=None):
    return make_list(list_obj or default)[0]


def get_keys(mapping, typ=None):
    typ = typ or set
    if isinstance(mapping, dict):
        mapping = mapping.keys()
    return typ(mapping)


def get_only_kwargs(varList, *args, **kwargs):
    new_kwargs = {}
    for i, arg in enumerate(args):
        key_variable = varList[i]
        kwargs[key_variable] = arg
    for key, value in kwargs.items():
        if key in varList:
            new_kwargs[key] = value
    return new_kwargs


def get_desired_key_values(obj, keys=None, defaults=None):
    defaults = defaults or {}
    if keys is None:
        return obj
    new_dict = {}
    for key, value in defaults.items():
        new_dict[key] = obj.get(key) or defaults.get(key)
    if obj and isinstance(obj, dict):
        for key in keys:
            new_dict[key] = obj.get(key) or defaults.get(key)
    return new_dict


def makeParams(*arg, **kwargs):
    arg = make_list(arg)
    arg.append({k: v for k, v in kwargs.items() if v is not None})
    return arg


def prune_inputs(func, *args, **kwargs):
    sig = inspect.signature(func)
    params = sig.parameters
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params.values())
    has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())
    new_args = list(args)
    new_kwargs = dict(kwargs)
    if "args" in new_kwargs:
        explicit_args = new_kwargs.pop("args")
        if isinstance(explicit_args, (list, tuple)):
            new_args.extend(explicit_args)
        else:
            new_args.append(explicit_args)
    if has_varargs:
        preferred_as_args = {"path", "file", "file_path", "filename", "value"}
        positional_candidates = []
        for k in list(new_kwargs.keys()):
            v = new_kwargs[k]
            if k in preferred_as_args:
                positional_candidates.append(v)
                del new_kwargs[k]
            elif isinstance(v, (str, int, float)) and len(positional_candidates) == 0:
                positional_candidates.append(v)
                del new_kwargs[k]
        new_args.extend(positional_candidates)
    if not has_varkw:
        allowed = {
            name for name, p in params.items()
            if p.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        }
        new_kwargs = {k: v for k, v in new_kwargs.items() if k in allowed}
    return tuple(new_args), new_kwargs


def run_pruned_func(func, *args, **kwargs):
    args, kwargs = prune_inputs(func, *args, **kwargs)
    return func(*args, **kwargs)


__all__ = [
    "get_sort", "combineList", "find_original_case", "ensure_nested_list",
    "make_list_add", "recursive_json_list", "filter_json_list_values",
    "get_highest_value_obj", "safe_list_return", "get_actual_number",
    "compare_lists", "remove_from_list", "list_set", "get_symetric_difference",
    "make_list_it", "get_single_from_list", "get_keys",
    "get_only_kwargs", "get_desired_key_values", "makeParams",
    "prune_inputs", "run_pruned_func",
]
