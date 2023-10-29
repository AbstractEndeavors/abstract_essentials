import json
import os
import requests
from abstract_utilities import (get_date,
                                get_time_stamp,
                                mkdirs,
                                safe_write_to_json,
                                json_key_or_default,
                                get_files,
                                unified_json_loader,
                                safe_json_loads,
                                safe_read_from_json,
                                
                                find_keys,
                                get_file_create_time,
                                
                                find_paths_to_key,

                                make_bool,
                                get_highest_value_obj,
                                make_list
                                )
from abstract_utilities.json_utils import safe_dump_to_file
from abstract_gui import get_browser
import nltk
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
    
    def safe_json_load(file):
        try:
            return json.load(file)
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

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
from nltk.tokenize import word_tokenize
def get_any_key(data,key):
    path_to_key = find_paths_to_key(safe_json_loads(data),key)
    if path_to_key:
        value = safe_json_loads(data)
        for each in path_to_key[0]:
            value = safe_json_loads(value[each])
        return value
    return path_to_key
class SaveManager:
    """
    Manages the saving of data. This class should provide methods to specify where (e.g., what database or file) and how (e.g., in what format) data should be saved.
    """
    def __init__(self,api_response={},title=None,directory=None):
        self.api_response=safe_json_loads(api_response)
        self.title = title
        self.model= get_any_key(self.api_response,'model') or 'default'
        self.created = get_any_key(self.api_response,'created')
        self.content = get_any_key(self.api_response,'content')
        self.generate_title = get_any_key(self.content,'generate_title')
        self.date = get_date()
        self.title = self.title or self.generate_title or self.created
        self.directory = mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        if get_any_key(self.content,'error'):
            self.fold_model= mkdirs(os.path.join(self.directory,self.date,'error'))
            self.file_name = f'{self.create_unique_title(title=self.title,directory=self.fold_model)}.json'
        
        else:

            self.fold_model= mkdirs(os.path.join(self.directory,self.date,self.model))
            self.file_name = f'{self.create_unique_title(title=self.title,directory=self.fold_model)}.json'
        self.file_path = os.path.join(self.fold_model,self.file_name)
        safe_dump_to_file(file_path=self.file_path,data=self.api_response)
    def create_unique_title(self,title:str=None,directory:str=None):
        """
        Generates a unique title by appending an index number to the given base title.

        Args:
            title (str, optional): The base title to start with. Defaults to a timestamp-based string.
            directory (str, optional): The directory to search for existing titles. Defaults to the current working directory.

        Returns:
            A unique title string formed by appending an index number to the base title.
        """
        title_new = title or self.title or str(get_time_stamp())
        directory = directory or self.directory or os.path.join(os.getcwd(),'response_data')
        files = get_files(directory)
        all_files = []
        for file in files:
            base_name = os.path.basename(file)
            all_files.append(base_name)
            file_name,ext=os.path.splitext(base_name)
            if file_name not in all_files:
                all_files.append(file_name)
        i=0
        while title_new in all_files:
            title_new=title+f'_{i}'
            i+=1
        return title_new

class ResponseManager:
    """
    Handles the management of responses received from the models. This could include interpreting and formatting the responses, managing errors, and handling special cases.
    """
    def __init__(self,prompt_mgr,api_mgr,title=None,directory=None):
        self.prompt_mgr=prompt_mgr
        self.model_mgr=self.prompt_mgr.model_mgr
        self.api_mgr=api_mgr
        self.title=title
        self.directory = mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        self.bot_notation=None
        self.token_dist =prompt_mgr.token_dist
        self.output=[]
        self.i_query=0
        self.query_done=False
    def post_request(self):
        """
        Sends a POST request to the specified endpoint with the provided prompt and headers.
        
        Args:
            endpoint (str): URL endpoint to which the request is sent.
            prompt (str or dict): Prompt or data to be sent in the request.
            content_type (str): Type of the content being sent in the request.
            api_key (str): The API key for authorization.
            header (dict): Optional custom headers. If not provided, default headers will be used.
            
        Returns:
            dict: Response received from the server.
        """
        if self.response.status_code == 200:
            print(f'Request successful with status code {self.api_response.status_code}')
        else:
            raise Exception(f'Request failed with status code {self.api_response.status_code}\n{self.api_response.text}\n\n')
        return self.get_response()
    def get_response(self):
        """
        Extracts and returns the response dictionary from the API response.

        Returns:
            dict: Extracted response dictionary.
        """
        try:
            self.api_response = self.response.json()
        except:
            self.api_response = self.response.text
        return self.api_response
    def try_load_response(self):
        self.api_response = safe_json_loads(self.get_response())
        self.content = safe_json_loads(find_keys(self.api_response,'content'))
        if self.content:
            if isinstance(self.content,list):
                self.content = safe_json_loads(self.content[0])
    def extract_response(self):
        self.query_js={}
        self.query_js["prompt"]=safe_json_loads(self.prompt)
        self.query_js["response"] = safe_json_loads(self.api_response)
        self.query_js["content"] = safe_json_loads(self.content)
        self.save_manager = SaveManager(api_response=self.api_response,title=self.title,directory=self.directory)
        self.output.append(self.api_response)
        return self.query_js
    def get_last_response(self):
        self.recent_file = get_highest_value_obj(get_files(self.directory),function=get_file_create_time)
        self.last_response = safe_json_loads(safe_read_from_json(self.recent_file))
        self.content = safe_json_loads(get_any_key(self.api_response,'content'))
        self.response_js= safe_json_loads(get_any_key(self.content, 'api_response'))
        return self.recent_file,self.response_js
    def get_response_bools(self):
        response_bool_js = {"abort":get_any_key(self.content, "abort") or False,
                            "additional_response":get_any_key(self.content, "additional_response") or False}
        for key,value in response_bool_js.items():
            if isinstance(value,str):
               response_bool_js[key]=eatAll(value,['\n','\t',' ',''])
            response_bool_js[key]=make_bool(response_bool_js[key])
        self.abort_it =response_bool_js['abort']
        self.additional_response_it = response_bool_js['additional_response']
        self.bot_notation = get_any_key(self.content, "notation")
    def send_query(self,i):
        self.prompt = self.prompt_mgr.create_prompt(dist_number=i,bot_notation=self.bot_notation)
        self.endpoint =self.model_mgr.selected_endpoint
        self.header=self.api_mgr.header
        self.response = requests.post(url=self.endpoint,json=self.prompt,headers=self.header)
        self.prepare_response()
    def test_query(self,i):
        self.response = self.get_last_response(file=test)[0]
        self.prepare_response(test=test)
    def prepare_response(self):
        self.try_load_response()
        self.extract_response()
        self.recent_file,self.response_js = self.get_last_response()
        self.get_response_bools()
    def initial_query(self):
        self.query_done=False
        self.i_query = 0
        for i in range(len(self.token_dist)):
            response_loop=True
            abort_it=False
            while response_loop:
                self.send_query(i)
                if not self.additional_response_it or self.abort_it:
                    response_loop = False
                    break
                print(f'in while {i}')
            if self.abort_it:
                break
            self.i_query=i
        self.query_done=True
        self.i_query=0
        return self.output

