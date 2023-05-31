#!/usr/bin/env python3
"""
json_utils.py
This script is a utility module providing functions for handling JSON data. It includes functionalities like:
1. Converting JSON strings to dictionaries.
2. Merging dictionaries, updating and removing keys.
3. Loading and saving JSON files.
4. Retrieving keys, values, and specific items from dictionaries.
5. Recursively displaying values of nested JSON data structures with indentation.

Each function is documented with Python docstrings for detailed usage instructions.
"""

from typing import Any, Dict, List, Union, Optional
import json

def convert_to_dict(obj: Union[str, Dict]) -> Union[Dict, Any]:
    """Convert a string representation of a dictionary to a dictionary.
    If the object is already a dictionary, it is returned as is."""
    if isinstance(obj, dict):
        return obj
    return json.loads(obj.replace("'",'"'))

def merge_dicts(js: Dict, js2: Dict) -> Dict:
    """Merge two dictionaries into one. If there are overlapping keys,
    the values from the second dictionary are used."""
    js.update(js2)
    return js

def remove_key(js: Dict, key: Any) -> Dict:
    """Remove a key from a dictionary. If the key is not present,
    no action is taken."""
    js.pop(key, None)
    return js

def update_key(js: Dict, jsN: Dict, key: Any) -> Dict:
    """If a key is present in the second dictionary, its value is
    copied over to the first dictionary."""
    if key in jsN:
        js[key] = jsN[key]
    return js

def add_to_dict(js: Dict, jsN: Dict) -> Dict:
    """For each key in the second dictionary, its value is copied
    over to the first dictionary."""
    for key in jsN.keys():
        js = update_key(js, jsN, key)
    return js


def get_keys(obj: Union[Dict, str]) -> List[Any]:
    """Get the keys of a dictionary. If the object is not a
    dictionary, an empty list is returned."""
    if not isinstance(obj, dict):
        return []
    return list(obj.keys())

def get_values(obj: Union[Dict, str]) -> List[Any]:
    """Get the values of a dictionary. If the object is not a
    dictionary, an empty list is returned."""
    if not isinstance(obj, dict):
        return []
    return list(obj.values())

def get_value(js: Union[List, Dict], key: Any) -> Any:
    """Get the value corresponding to a key in a dictionary or list.
    If the key is not present, False is returned."""
    if key in js:
        return js[key]
    return False

def get_key_from_value(js: Dict, st: Any, default: Any) -> Any:
    """Get the key corresponding to a value in a dictionary.
    If the value is not present, a default value is returned."""
    for key, value in js.items():
        if st in value:
            return key
    return default

def get_specific_key(js: Dict, i: int) -> Any:
    """Get the i-th key of a dictionary."""
    return list(js.keys())[i]

def get_specific_item(js: Dict, i: int, k: int) -> Any:
    """Get the k-th value of the i-th key in a dictionary."""
    return js[get_specific_key(js, i)][k]

def display_values(json_obj: Union[Dict, List], indent: int = 0) -> None:
    """Recursively print the keys and values of a dictionary or list.
    Nested structures are indented."""
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, (dict, list)):
                print('  ' * indent + f"{key}:", end='')
                display_values(value, indent + 1)
            else:
                print('  ' * indent + f"{key}: {value}")
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            if isinstance(item, (dict, list)):
                print('  ' * indent + f"[{index}]:", end='')
                display_values(item, indent + 1)
            else:
                print('  ' * indent + f"[{index}]: {item}")
import json

def save_json_value(json_data:dict, keys:list, value:any):
    """
    Update the JSON data with the given keys and value.
    If the keys don't exist, they will be created.
    
    Args:
        json_data (dict): The JSON data to update.
        keys (list): A list of keys representing the path to the value.
        value (any): The value to be saved.
        
    Returns:
        dict: The updated JSON data.
    """
    current_level = json_data
    
    # Traverse the keys path, creating any missing keys
    for key in keys[:-1]:
        if key not in current_level:
            current_level[key] = {}
        current_level = current_level[key]
    
    # Save the value at the final key
    current_level[keys[-1]] = value
    
    return json_data

def find_keys(data:any, target_keys:list):
    values = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key in target_keys:
                values.append(value)
            values.extend(find_keys(value, target_keys))
    elif isinstance(data, list):
        for item in data:
            values.extend(find_keys(item, target_keys))
    return values
def invert_json(json_data):
    """
    Inverts a JSON dictionary where the keys are token numbers and the values are lists of model names.

    Args:
        json_data (dict): The JSON dictionary to invert.

    Returns:
        dict: The inverted JSON dictionary, where the keys are model names and the values are token numbers.
    """
    inverted_data = {}
    for token_num, model_names in json_data.items():
        for model_name in model_names:
            inverted_data[model_name] = token_num
    return inverted_data

def get_from_lsJs(js, st, default):
    """
    Searches for a given value 'st' within lists in a JSON dictionary and returns the corresponding key.

    Args:
        js (dict): The JSON dictionary to search within.
        st (any): The value to search for.
        default (any): The default value to return if 'st' is not found.

    Returns:
        any: The key associated with the first occurrence of 'st' in the lists of the JSON dictionary,
             or 'default' if 'st' is not found.
    """
    keys = get_keys(js)
    for k in range(0, len(keys)):
        key = keys[k]
        ls = js[key]
        if st in ls:
            return key
    return default
# Function: convert_to_dict
# Function: merge_dicts
# Function: remove_key
# Function: update_key
# Function: add_to_dict
# Function: load_from_file
# Function: dump_to_str
# Function: dump_to_file
# Function: get_keys
# Function: get_values
# Function: get_value
# Function: get_key_from_value
# Function: get_specific_key
# Function: get_specific_item
# Function: display_values
