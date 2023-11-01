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
import json
import re
import os
from typing import List, Union, Dict, Any
def json_key_or_default(json_data,key,default_value):
    json_data = safe_json_loads(json_data)
    if not isinstance(json_data,dict) or (isinstance(json_data,dict) and key not in json_data):
        return default_value
    return json_data[key]

def create_and_read_json(file_path: str, json_data: dict = None, error=False, error_msg=True) -> dict:
    """
    Create a JSON file if it does not exist, then read from it.
    
    Args:
        file_path (str): The path of the file to create and read from.
        json_data (dict): The content to write to the file if it does not exist.
        
    Returns:
        dict: The contents of the JSON file.
    """
    if error_msg == True:
        error_msg = f"{file_path} does not exist; creating file with default_data"
    try_read = safe_read_from_json(file_path, default_value=None)
    if try_read is None and json_data is not None:
        safe_dump_to_file(file_path=file_path, data=json_data)
    return safe_read_from_json(file_path=file_path)

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
def get_error_msg(error_msg, default_error_msg):
    return error_msg if error_msg else default_error_msg

def safe_dump_to_file(data, file_path, ensure_ascii=False, indent=4):
    if isinstance(data, (dict, list, tuple)):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(data))

def safe_write_to_json(file_path, data, ensure_ascii=False, indent=4, error=False, error_msg=None):
    temp_file_path = f"{file_path}.temp"
    var_data = {"file_path": temp_file_path, "instance": 'w'}
    error_msg = get_error_msg(error_msg, f"Error writing JSON to '{file_path}'")
    
    open_it = all_try(var_data=var_data, function=open, error_msg=error_msg)
    
    if open_it:
        with open_it as file:
            safe_dump_to_file(data, file, ensure_ascii=ensure_ascii, indent=indent)
    
        os.replace(temp_file_path, file_path)

def safe_read_from_json(file_path: str, default_value: Any = None, error: bool = False, error_msg: str = None) -> Any:
    """
    Safely read data from a JSON file. If the file reading or JSON decoding fails, returns the default value.

    Args:
        file_path (str): The path of the file to read.
        default_value (Any): The value to return if reading or decoding fails. Default is None.
        error (bool): Whether to raise an exception if an error occurs. Default is False.
        error_msg (str): Custom error message to display if an error occurs.

    Returns:
        Any: The decoded JSON data or the default value if reading or decoding fails.
    """
    if not os.path.exists(file_path):
        if error:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        if error_msg:
            print(error_msg)
        return default_value

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    try:
        return json.loads(file_content)
    except json.JSONDecodeError as e:
        if error:
            raise e
        if error_msg:
            print(error_msg, f': {e}')
        return default_value
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

def try_json_loads(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
    
def try_json_load(file):
    try:
        return json.load(file)
    except json.JSONDecodeError:
        return None

def unified_json_loader(file_path, default_value=None, encoding='utf-8'):
    # Try to load from the file
    with open(file_path, 'r', encoding=encoding) as file:
        content = all_try(data=file, function=try_json_load, error_value=json.JSONDecodeError, error=False)
    
    if isinstance(content, dict):
        return content
    
    # Try to load from the file as a string
    with open(file_path, 'r', encoding=encoding) as file:
        content_str = file.read()
        content = all_try(data=content_str, function=try_json_loads, error_value=json.JSONDecodeError, error=False)
    
    if isinstance(content, dict):
        return content
    
    print(f"Error reading JSON from '{file_path}'.")
    return default_value


def get_key_values_from_path(json_data, path):
    try_path = get_value_from_path(json_data, path[:-1])
    if isinstance(try_path, dict):
        return list(try_path.keys())
    
    current_data = json_data
    for step in path:
        try:
            current_data = current_data[step]
            if isinstance(current_data, str):
                try:
                    current_data = json.loads(current_data)
                except json.JSONDecodeError:
                    pass
        except (TypeError, KeyError, IndexError):
            return None
    
    if isinstance(current_data, dict):
        return list(current_data.keys())
    else:
        return None
def convert_to_json(obj):
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        return safe_json_loads(obj)
    return None
def get_any_key(data,key):
    path_to_key = find_paths_to_key(safe_json_loads(data),key)
    if path_to_key:
        value = safe_json_loads(data)
        for each in path_to_key[0]:
            value = safe_json_loads(value[each])
        return value
    return path_to_key

def all_try(function=None, data=None, var_data=None, error=False, error_msg=None, error_value=Exception, attach=None, attach_var_data=None):
    try:
        if not function:
            raise ValueError("Function is required")

        if var_data and not data:
            result = function(**var_data)
        elif data and not var_data:
            if attach and attach_var_data:
                result = function(data).attach(**attach_var_data)
            else:
                result = function(data).attach() if attach else function(data)
        elif data and var_data:
            raise ValueError("Both data and var_data cannot be provided simultaneously")
        else:
            result = function()

        return result
    except error_value as e:
        if error:
            raise e
        elif error_msg:
            print_error_msg(error_msg, f': {e}')
        return False
def all_try_json_loads(data, error=False, error_msg=None, error_value=(json.JSONDecodeError, TypeError)):
    return all_try(data=data, function=json.loads, error=error, error_msg=error_msg, error_value=error_value)

def safe_json_loads(data, default_value=None, error=False, error_msg=None): 
    """ Safely attempts to load a JSON string. Returns the original data or a default value if parsing fails.
    Args:
        data (str): The JSON string to parse.
        default_value (any, optional): The value to return if parsing fails. Defaults to None.
        error (bool, optional): Whether to raise an error if parsing fails. Defaults to False.
        error_msg (str, optional): The error message to display if parsing fails. Defaults to None.
    
    Returns:
        any: The parsed JSON object, or the original data/default value if parsing fails.
    """
    try_json = all_try_json_loads(data=data, error=error, error_msg=error_msg)
    if try_json:
        return try_json
    if default_value:
        data = default_value
    return data
def clean_invalid_newlines(json_string: str,line_replacement_value='') -> str: 
    """ Removes invalid newlines from a JSON string that are not within double quotes.
    Args:
        json_string (str): The JSON string containing newlines.
    
    Returns:
        str: The JSON string with invalid newlines removed.
    """
    pattern = r'(?<!\\)\n(?!([^"]*"[^"]*")*[^"]*$)'
    return re.sub(pattern, line_replacement_value, json_string)
def get_value_from_path(json_data, path,line_replacement_value='*n*'): 
    """ Traverses a nested JSON object using a specified path and returns the value at the end of that path.
    Args:
        json_data (dict/list): The JSON object to traverse.
        path (list): The path to follow in the JSON object.
    
    Returns:
        any: The value at the end of the specified path.
    """
    current_data = safe_json_loads(json_data)
    for step in path:
        current_data = safe_json_loads(current_data[step])
        if isinstance(current_data, str):
            current_data = read_malformed_json(current_data,line_replacement_value=line_replacement_value)
    return current_data
def find_paths_to_key(json_data, key_to_find,line_replacement_value='*n*'): 
    """ Searches a nested JSON object for all paths that lead to a specified key.
    Args:
        json_data (dict/list): The JSON object to search.
        key_to_find (str): The key to search for in the JSON object.
    
    Returns:
        list: A list of paths (each path is a list of keys/indices) leading to the specified key.
    """
    def _search_path(data, current_path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    paths.append(new_path)
                if isinstance(value, str):
                    try:
                        json_data = read_malformed_json(value,line_replacement_value=line_replacement_value)
                        _search_path(json_data, new_path)
                    except json.JSONDecodeError:
                        pass
                _search_path(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                _search_path(item, new_path)
    
    paths = []
    _search_path(json_data, [])
    return paths
def read_malformed_json(json_string,line_replacement_value="*n"): 
    """ Attempts to parse a malformed JSON string after cleaning it.
    Args:
        json_string (str): The malformed JSON string.
    
    Returns:
        any: The parsed JSON object.
    """
    if isinstance(json_string, str):
        json_string = clean_invalid_newlines(json_string,line_replacement_value=line_replacement_value)
    return safe_json_loads(json_string)
def get_any_value(json_obj, key,line_replacement_value="*n*"): 
    """ Fetches the value associated with a specified key from a JSON object or file. If the provided input is a file path, it reads the file first.
    Args:
        json_obj (dict/list/str): The JSON object or file path containing the JSON object.
        key (str): The key to search for in the JSON object.
    
    Returns:
        any: The value associated with the specified key.
    """
    if os.path.isfile(json_obj):
        with open(json_obj, 'r', encoding='UTF-8') as f:
            json_obj=f.read()
    json_data = read_malformed_json(json_obj)
    paths_to_value = find_paths_to_key(json_data, key)
    if not isinstance(paths_to_value, list):
        paths_to_value = [paths_to_value]
    for i, path_to_value in enumerate(paths_to_value):
        paths_to_value[i] = get_value_from_path(json_data, path_to_value)
        if isinstance(paths_to_value[i],str):
            paths_to_value[i]=paths_to_value[i].replace(line_replacement_value,'\n')
    if len(paths_to_value) == 1:
        paths_to_value = paths_to_value[0]
    return paths_to_value
