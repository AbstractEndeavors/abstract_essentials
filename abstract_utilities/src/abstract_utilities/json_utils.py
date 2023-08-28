#!/usr/bin/env python3
"""
json_utils.py

This script is a utility module providing functions for handling JSON data. It includes functionalities like:
1. Converting JSON strings to dictionaries and vice versa.
2. Merging, adding to, updating, and removing keys from dictionaries.
3. Retrieving keys, values, specific items, and key-value pairs from dictionaries.
4. Recursively displaying values of nested JSON data structures with indentation.
5. Loading from and saving dictionaries to JSON files.
6. Validating and cleaning up JSON strings.
7. Searching and modifying nested JSON structures based on specific keys, values, or paths.
8. Inverting JSON data structures.
9. Creating and reading from JSON files.

Each function is documented with Python docstrings for detailed usage instructions.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
from typing import Union
import json
import re
def convert_to_dict(obj: Union[str, dict]) -> Union[dict, any]:
    """
    Convert a string representation of a dictionary to a dictionary.
    If the object is already a dictionary, it is returned as is.

    Args:
        obj (Union[str, dict]): The object to be converted.

    Returns:
        Union[dict, any]: The converted dictionary.
    """
    if isinstance(obj, dict):
        return obj
    return json.loads(obj.replace("'",'"'))

def merge_dicts(json_data: Dict, json_data_2: dict) -> dict:
    """
    Merge two dictionaries into one. If there are overlapping keys,
    the values from the second dictionary are used.
    
    Args:
        json_data (Dict): The first dictionary.
        json_data_2 (dict): The second dictionary.

    Returns:
        dict: The merged dictionary.
    """
    json_data.update(json_data_2)
    return js

def remove_key(json_data: dict, key: any) -> dict:
    """
    Remove a key from a dictionary. If the key is not present,
    no action is taken.
    
    Args:
        json_data (dict): The dictionary.
        key (any): The key to remove.

    Returns:
        dict: The modified dictionary.
    """
    json_data.pop(key, None)
    return json_data

def update_key(json_data: dict, json_data_2: dict, key: any) -> dict:
    """
    If a key is present in the second dictionary, its value is
    copied over to the first dictionary.
    
    Args:
        json_data (dict): The first dictionary.
        json_data_2 (dict): The second dictionary.
        key (any): The key to update.

    Returns:
        dict: The modified dictionary.
    """
    if key in jsN:
        json_data[key] = json_data_2[key]
    return js

def add_to_dict(json_data: dict, json_data_2: dict) -> dict:
    """
    For each key in the second dictionary, its value is copied
    over to the first dictionary.
    
    Args:
        json_data (dict): The first dictionary.
        json_data_2 (dict): The second dictionary.

    Returns:
        dict: The modified dictionary.
    """
    for key in json_data_2.keys():
        json_data = update_key(json_data, json_data_2, key)
    return json_data


def get_keys(json_data: Union[dict, str]) -> List[any]:
    """
    Get the keys of a dictionary. If the object is not a
    dictionary, an empty list is returned.
    
    Args:
        json_data (Union[dict, str]): The dictionary or JSON string.

    Returns:
        List[any]: A list of keys.
    """
    if not isinstance(json_data, dict):
        return []
    return list(json_data.keys())

def get_values(json_data: Union[dict, str]) -> List[Any]:
    """
    Get the values of a dictionary. If the object is not a
    dictionary, an empty list is returned.
    
    Args:
        json_data (Union[dict, str]): The dictionary or JSON string.

    Returns:
        List[Any]: A list of values.
    """
    if not isinstance(json_data, dict):
        return []
    return list(json_data.values())

def get_value(json_data: Union[dict, str], key: any) -> any:
    """
    Get the value corresponding to a key in a dictionary or list.
    If the key is not present, False is returned.
    
    Args:
        json_data (Union[dict, str]): The dictionary or JSON string.
        key (any): The key to retrieve.

    Returns:
        any: The value corresponding to the key, or False if key is not present.
    """
    if key in json_data:
        return json_data[key]
    return False

def get_key_from_value(json_data: dict, string: any, default: any) -> any:
    """
    Get the key corresponding to a value in a dictionary.
    If the value is not present, a default value is returned.
    
    Args:
        json_data (dict): The dictionary.
        string (any): The value to search for.
        default (any): The default value to return if not found.

    Returns:
        any: The key corresponding to the value, or the default value if not found.
    """
    for key, value in json_data.items():
        if string in value:
            return key
    return default

def get_specific_key(json_data: Dict, i: int) -> any:
    """
    Get the i-th key of a dictionary.
    
    Args:
        json_data (Dict): The dictionary.
        i (int): The index of the key to retrieve.

    Returns:
        any: The i-th key.
    """

    return list(json_data.keys())[i]

def get_specific_item(json_data: dict, i: int, k: int) -> any:
    """
    Get the k-th value of the i-th key in a dictionary.
    
    Args:
        json_data (dict): The dictionary.
        i (int): The index of the key.
        k (int): The index of the value within the key's list.

    Returns:
        any: The k-th value of the i-th key.
    """
    return json_data[get_specific_key(js, i)][k]

def display_values(json_obj: Union[Dict, List], indent: int = 0) -> None:
    """
    Recursively print the keys and values of a dictionary or list.
    Nested structures are indented.
    
    Args:
        json_obj (Union[Dict, List]): The dictionary or list to display.
        indent (int): The indentation level for nested structures.
    """
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
                
def save_json_value(json_data: dict, keys: list, value: any) -> dict:
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

def find_keys(data: Union[dict,list], target_keys: list) -> list:
    """
    Searches recursively for all values associated with specific keys in a JSON-like structure.

    Args:
        data (dict or list): The JSON-like structure to search.
        target_keys (list): List of keys for which associated values need to be fetched.

    Returns:
        list: List of values associated with the target keys.
    """
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
def invert_json(json_data: dict) -> dict:
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

def get_from_lsJs(json_data: dict, string: any, default: any) -> any:
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
    for each in get_keys(json_data):
        if string in json_data[each]:
            return each
    return default
def clean_invalid_newlines(json_string: str) -> str:
    """
    Removes invalid newlines from a JSON string that are not within double quotes.

    Args:
        json_string (str): The JSON string containing newlines.

    Returns:
        str: The JSON string with invalid newlines removed.
    """
    # This regex will match any newline that is not within double quotes.
    pattern = r'(?<!\\)\n(?!([^"]*"[^"]*")*[^"]*$)'
    return re.sub(pattern, '', json_string)
def is_valid_json(json_string: str) -> bool:
    """
    Checks whether a given string is a valid JSON string.

    Args:
        json_string (str): The string to check.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    try:
        json_obj = json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False
def find_value_by_key_path(json_data: dict, key_path: Union[list, str]) -> Union[list, None]:
    """
    Finds the value in a JSON-like structure given a specific key path.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key_path (list): A list of keys representing the path to the desired value.

    Returns:
        The value found at the specified key path, or None if not found.
    """
    def search_in_path(data, keys):
        for key in keys:
            if isinstance(data, dict):
                if key in data:
                    data = data[key]
                else:
                    return find_values_by_key(data, key)
            elif isinstance(data, list):
                try:
                    index = int(key)
                    data = data[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return data

    value = search_in_path(json_data, list(key_path))
    return value

def find_values_by_key(json_data: dict, key: str) -> list:
    """
    Finds all values in a JSON-like structure associated with a specific key.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key (str): The key to search for.

    Returns:
        list: A list of dictionaries containing the path of keys leading to each value and the value itself.
    """
    result = []
    def search_in_json(data, keys=[]):
        if isinstance(data, dict):
            if key in data:
                result.append({"keys": keys + [key], "value": data[key]})
            for sub_key, value in data.items():
                search_in_json(value, keys + [sub_key])
        elif isinstance(data, list):
            for index, item in enumerate(data):
                search_in_json(item, keys + [str(index)])
    search_in_json(json_data)
    return result
def find_path_to_key(json_data: dict, key_to_find: str) -> list:
    """
    Finds the path to a specific key within a JSON-like structure.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key_to_find (str): The key to find the path for.

    Returns:
        list: A list of keys representing the path to the specified key, or None if the key is not found.
    """
    def search_path(data, current_path=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    return new_path
                found_path = search_path(value, new_path)
                if found_path:
                    return found_path
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                found_path = search_path(item, new_path)
                if found_path:
                    return found_path
        return None

    path = search_path(json_data)
    return path
def find_path_to_value(json_data: any, value_to_find: any) -> list:
    """
    Finds the path to a specific value within a JSON-like structure.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        value_to_find: The value to find the path for.

    Returns:
        list: A list of keys representing the path to the specified value, or None if the value is not found.
    """

    def search_path(data, current_path=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if value == value_to_find:
                    return new_path
                found_path = search_path(value, new_path)
                if found_path:
                    return found_path
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                if item == value_to_find:
                    return new_path
                found_path = search_path(item, new_path)
                if found_path:
                    return found_path
        return None

    path = search_path(json_data)
    return path
def load_from_file(file_path: str) -> Union[dict, any]:
    """
    Load a dictionary from a file. The file should contain a
    JSON representation of the dictionary.
    
    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Union[dict, any]: The loaded dictionary.
    """
    with open(file_path, 'r') as f:
        return json.load(f)
def dump_to_file(file_path: str, json_data: dict) -> None:
    """
    Write a dictionary to a file in JSON format.
    
    Args:
        file_path (str): The path to the output file.
        json_data (dict): The dictionary to be written.

    Returns:
        None
    """
    with open(file_path, 'w') as f:
        json.dump(json_data, f)
def dump_to_str(json_data: dict) -> str:
    """
    Convert a dictionary to a JSON string.
    
    Args:
        json_data (dict): The dictionary to convert.

    Returns:
        str: The JSON string representation of the dictionary.
    """
    return json.dumps(json_data)
def create_and_read_json(file_path: str, json_data: dict = {}) -> dict:
    """
    Create a json file if it does not exist, then read from it.
    
    Args:
        file_path (str): The path of the file to create and read from.
        json_data (dict): The content to write to the file if it does not exist.
        
    Returns:
        dict: The contents of the json file.
    """
    if not os.path.isfile(file_path):
        dump_to_file(file_path, json_data)
    return load_from_file(file_path)
