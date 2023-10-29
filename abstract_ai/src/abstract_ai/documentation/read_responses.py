from abstract_utilities import *
import json
from typing import Any
def json_key_or_default(json_data,key,default_value):
    json_data = safe_json_loads(json_data)
    if not isinstance(json_data,dict) or (isinstance(json_data,dict) and key not in json_data):
        return default_value
    return json_data[key]
def try_json_loads(data, error=False, error_msg=None, error_value=(json.JSONDecodeError, TypeError)):
    return all_try(data=data, function=json.loads, error=error, error_msg=error_msg, error_value=error_value)

def safe_dump_to_file(file_path, data, ensure_ascii=False, indent=4):
    if isinstance(data, (dict, list, tuple)):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)
    else:
        file.write(str(data))

def all_try(function=None, data=None, var_data=None, error=False, error_msg=None, error_value=None, attach=None, attach_var_data=None):
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
def safe_json_loads(data,default_value=None,error=False,error_msg=None):
    try_json = try_json_loads(data=data,error=error,error_msg=error_msg)
    if try_json:
        return try_json
    if default_value:
        data = default_value
    return data
def unified_json_loader(file_path, default_value=None, encoding='utf-8'):
    def safe_json_loads(data):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None
    
    def safe_json_load(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    content = all_try(var_data={"file_path": file_path}, function=safe_json_load,error_value=json.JSONDecodeError, error=False)
    
    if isinstance(content, dict):
        return content
    
    content = all_try(var_data={"file_path": file_path}, function=safe_json_loads, error_value=json.JSONDecodeError,error=False)
    
    if isinstance(content, dict):
        return content
    
    print(f"Error reading JSON from '{file_path}'.")
    return default_value

def find_paths_to_key(json_data, key_to_find):
    def _search_path(data, current_path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    paths.append(new_path)
                
                if isinstance(value, str):
                    try:
                        parsed_json = json.loads(value)
                        _search_path(parsed_json, new_path)
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

def get_value_from_path(json_data, path):
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
    return current_data

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
def if_key_return_other(key,key_list):
    new_list=[key]
    for each_key in key_list:
        if each_key != key:
            return each_key
def safe_list_return(current_list,list_num=0):
    if len(current_list) >= list_num+1:
        return current_list[int(list_num)]
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
import os
def find_paths_to_key(json_data: dict, key_to_find: str) -> list:
    """
    Finds all paths to a specific key within a JSON-like structure.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key_to_find (str): The key to find paths for.

    Returns:
        list: A list of lists, where each inner list represents a path to the specified key.
    """
    paths = []

    def search_path(data, current_path=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    paths.append(new_path)
                
                # Check if the value is a JSON string
                if isinstance(value, str):
                    try:
                        parsed_json = json.loads(value)
                        search_path(parsed_json, new_path)
                    except json.JSONDecodeError:
                        pass
                
                search_path(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                search_path(item, new_path)

    search_path(json_data)
    return paths
def get_value_from_path(json_data: dict, path: list):
    """
    Retrieves a value from a JSON-like structure given a path.

    Args:
        json_data (dict or list): The JSON-like structure to retrieve the value from.
        path (list): The path to the value, represented as a list of keys and indices.

    Returns:
        The value at the specified path, or None if the path is not valid.
    """
    current_data = json_data
    for step in path:
        try:
            # Navigate using the key/index from the path
            current_data = current_data[step]
            
            # Check if the current data is a string that can be parsed as JSON
            if isinstance(current_data, str):
                try:
                    current_data = json.loads(current_data)
                except json.JSONDecodeError:
                    pass
        except (TypeError, KeyError, IndexError):
            return None
    return current_data
def get_any_key(data,key):
    path_to_key = find_paths_to_key(safe_json_loads(data),key)
    if path_to_key:
        value = safe_json_loads(data)
        for each in path_to_key[0]:
            value = safe_json_loads(value[each])
        return value
    return path_to_key
responses = """C:/Users/jrput/Downloads/response_data/2023-10-27/gpt-4-0613/1698434723.json"""
for file in responses.split('\n'):
    basename,ext = os.path.splitext(file)
    if ext=='.json':
        response = safe_read_from_json(file)
        content = get_value_from_path(response,find_paths_to_key(response,'choices')[0])
        content = get_value_from_path(content,find_paths_to_key(content,'content')[0])
        api_response=get_value_from_path(content,get_any_key(content,'api_response'))
        print(api_response)
        if isinstance(safe_json_loads(api_response),dict):
            for key,value in safe_json_loads(api_response).items():
                print(key)
                print(value)
                if isinstance(safe_json_loads(value),dict):
                    for key2,value2 in safe_json_loads(value).items():
                        print(key2)
                        print(value2)
