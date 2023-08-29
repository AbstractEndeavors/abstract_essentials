"""
response_handling.py
=====================
This module is part of the `abstract_ai` module of the `abstract_essentials` package. It provides comprehensive utilities for processing and managing the responses obtained from the OpenAI API. It also offers tools for aggregating, saving, and analyzing the data.

Functions:
----------
- create_unique_title(): Generates a unique title for saving responses, ensuring there's no overwrite.
- save_response(): Saves the JSON response from the API call to a structured directory.
- find_keys(): Recursively finds values associated with specified keys in nested dictionaries or lists.
- print_it(): Prints the provided string and returns it.
- aggregate_conversations(): Aggregates conversation data from multiple JSON files within a directory.
- get_responses(): Retrieves and processes aggregated conversations from JSON files.
- get_response(): Retrieves specific details about an OpenAI API endpoint from the response.

Notes:
------
This module also contains hidden functionalities (or "hidden gems") that can be handy for specific purposes. While the code provides a robust foundation for handling API responses, ensure you adjust the settings and configurations to suit your specific needs.

About abstract_ai
--------------------
part of: abstract_ai
Version: 0.1.7.1
Author: putkoff
Contact: partners@abstractendeavors.com
Content Type: text/markdown
Source and Documentation:
For the source code, documentation, and more details, visit the official GitHub repository.
github: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai

Notes:
------
The utilities provided in this module are closely tied to the format and structure of the OpenAI API responses. Ensure you have the right environment setup and dependencies for the module to function correctly.
"""
import json
import os
from abstract_utilities.path_utils import path_join, mkdirs,get_file_create_time,split_text
from abstract_utilities.time_utils import get_time_stamp,get_date
from abstract_utilities.read_write_utils import write_to_file
from abstract_utilities.json_utils import find_values_by_key,find_value_by_key_path,find_path_to_value,find_path_to_key
from .endpoints import get_endpoint_defaults
from abstract_gui import get_browser
def create_unique_title(title:str=str(get_time_stamp()),directory:str=os.getcwd()):
    """
    Generates a unique title by appending an index number to the given base title.

    Args:
        title (str, optional): The base title to start with. Defaults to a timestamp-based string.
        directory (str, optional): The directory to search for existing titles. Defaults to the current working directory.

    Returns:
        A unique title string formed by appending an index number to the base title.
    """
    dir_list = os.listdir(directory)
    for i,each in enumerate(dir_list):
        dir_list[i] = split_text(each)[0]
    if title not in dir_list:
        return title
    i=0
    while title+'_'+str(i) in dir_list:
        i+=1
    return title+'_'+str(i)
def save_response(prompt_js:dict={},endpoint:str=None,response:(dict or str)=None, title:str=None,directory:str=None):
    """
    Saves the response JSON and generated text to a file.

    Args:
        js (dict): The input JSON dictionary.
        response (dict): The response dictionary.
        title (str, optional): The title for the file. Defaults to the current timestamp.

    Returns:
        str: The generated text.
    """
    if directory == None:
        directory = 'response_data'
    if title == None:
        title= str(get_time_stamp())
    if endpoint == None and "endpoint" in prompt_js:
        endpoint = prompt_js["endpoint"]
    if response == None:
        return {}
    try:
        prompt_js['response'] = response.json()
    except:
        prompt_js['response'] =response
    try:
        prompt_js['output'] = get_response(json_data=prompt_js['response'],endpoint=endpoint)
        if 'title' in prompt_js:
            title = prompt_js['title']
    except:
        prompt_js['output'] = False
    path = mkdirs(path_join(mkdirs(path_join(mkdirs(directory), get_date())), prompt_js['model']))
    title=create_unique_title(title=title,directory=mkdirs(path))
    write_to_file(filepath=path_join(path, title + '.json'), contents=json.dumps(prompt_js))
    return prompt_js
def find_keys(data, target_keys):
    """
    Finds the values associated with the specified target keys in a nested dictionary or list.

    Args:
        data (dict or list): The nested dictionary or list to search within.
        target_keys (list): The list of keys to search for.

    Returns:
        list: A list of values associated with the target keys.
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


def print_it(string):
    """
    Prints the input string and returns it.

    Args:
        st (str): The string to be printed.

    Returns:
        str: The input string.
    """
    print(string)
    return string
def aggregate_conversations(directory:str=None):
    """
    Aggregates conversations from JSON files in the specified directory.

    Args:
        directory (str): The directory containing the JSON files.

    Returns:
        list: A list of aggregated conversations.
    """
    if directory == None:
        directory = get_browser('please choose a directory to search for the raw data files')
    json_files, lsAll = [], []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file = os.path.join(root, file)
                json_files.append((get_file_create_time(file), file))
    sorted_json_files = sorted(json_files, key=lambda x: x[0])
    aggregated_conversations = []
    chat_log_file = open("chat_log.txt", "w")
    model = 'gpt'
    for file in sorted_json_files:
        with open(file[1], "r") as f:
            data = json.load(f)
            relevant_values = find_keys(data, ['messages', 'prompt', 'content'])
            for i, value in enumerate(relevant_values):
                while type(value) is list:
                    value = value[0]
                if type(value) is dict:
                    if 'model' in value:
                        model = value['model']
                    if 'prompt' in value:
                        lsAll.append({print_it("user"): print_it(value["prompt"])})
                    if 'content' in value:
                        lsAll.append({print_it(model): print_it(value['content'])})
                print(lsAll)
    chat_log_file.close()
    return aggregated_conversations
def get_responses(path):
    """
    Retrieves the aggregated conversations from JSON files.

    If the 'response_data' directory does not exist in the current working directory, prompts the user to select a directory
    containing the JSON files. Otherwise, uses the 'response_data' directory.

    Returns:
        None
    """
    if "response_data" not in os.listdir(path):
        aggregate_conversations(get_browser())
    else:
        aggregate_conversations(get_browser())#path_join(path,"response_data"))
def get_response(endpoint:str,json_data:dict=get_endpoint_defaults(),endpoint_subsection:str=None,param:(str)="response_key"):
    """
    Retrieves information about a specific OpenAI API endpoint.

    Args:
        endpoint (str): The endpoint name to retrieve information for.
        endpoint_subsection (str, optional): The subsection of the endpoint (if applicable).
        param (str, optional): The parameter to retrieve from the response.

    Returns:
        The retrieved information for the specified endpoint and parameter.
    """
    key_path = find_path_to_value(get_endpoint_defaults(),value_to_find=endpoint)
    if key_path is None:
        key_path = find_path_to_key(get_endpoint_defaults(),endpoint)
    if key_path[-1] != endpoint_subsection and endpoint_subsection is not None:
        key_path.append(endpoint_subsection)
    response = find_value_by_key_path(json_data,key_path)
    key_path[-1]=param
    if param == "response_key":
        response_key = find_value_by_key_path(get_endpoint_defaults(),key_path)
        if isinstance(response_key,list):
            if isinstance(response_key[0],dict):
                if "value" in response_key[0]:
                    response_key = response_key[0]["value"]
        response=find_value_by_key_path(json_data,[response_key])[0]["value"]
    return response
