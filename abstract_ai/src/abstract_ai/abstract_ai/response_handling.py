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
import requests
from abstract_utilities import (get_date,
                                get_time_stamp,
                                mkdirs,
                                safe_write_to_json,
                                json_key_or_default,
                                get_files,
                                
                                safe_json_loads,
                                safe_read_from_json,
                                safe_write_to_json,
                                find_keys,
                                get_file_create_time,
                                get_open,
                                
                                find_path_to_value,
                                find_path_to_key,
                                find_value_by_key_path,
                                make_bool,
                                get_highest_value_obj
                                )
from .endpoints import get_endpoint_defaults
from abstract_gui import get_browser
class SaveResponses:
    def __init__(self,query_js,title=None,directory=None):
        self.query_js=query_js
        self.title = title or json_key_or_default(obj=self.query_js["content"],key='title',default=self.query_js["response"]['created'])
        self.directory = mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        self.fold_model=self.create_directory()
        self.file_name=self.create_title()
        self.file_path = os.path.join(self.fold_model,self.file_name)
        safe_write_to_json(file_path=self.file_path,data=self.query_js)
    def create_directory(self):
        self.fold_date = mkdirs(os.path.join(self.directory,get_date()))
        self.fold_model = mkdirs(os.path.join(self.fold_date,self.query_js["response"]['model']))
        return self.fold_model
    def create_title(self):
        self.title = self.create_unique_title(title=self.title,directory=self.fold_model)
        self.file_name =  f'{self.title}.json'
        return self.file_name
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
    def __init__(self,endpoint,prompt,header,title=None,directory=None):
        self.endpoint =endpoint
        self.prompt=prompt
        self.header=header
        self.response = requests.post(url=self.endpoint,json=self.prompt,headers=self.header)
        self.api_response = safe_json_loads(self.get_response())
        self.content = safe_json_loads(find_keys(self.api_response,'content'))
        if isinstance(self.content,list):
            self.content = safe_json_loads(self.content[0])
        self.query_js=self.extract_response()
        self.title=title
        self.directory=directory
        self.save_manager = SaveResponses(query_js=self.query_js,title=self.title,directory=self.directory)
        self.recent_file,self.response_js = self.get_last_response()
        self.abort_it,self.additional_response_it,self.bot_notation=self.get_response_bools()
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
            resp = self.self.response.json()
            return resp
        except:
            return self.response.text
    def extract_response(self):
        self.query_js={}
        self.query_js["prompt"]=self.prompt
        self.query_js["response"] = self.api_response
        self.query_js["content"] = self.content
        return self.query_js
    def get_last_response(self):
        self.recent_file = get_highest_value_obj(get_files(self.save_manager.directory),function=get_file_create_time)
        self.last_response = safe_read_from_json(self.recent_file)
        self.last_response=safe_json_loads(self.last_response)
        self.response_js= find_keys(self.last_response, 'ai_response_choices')
        if isinstance(self.response_js,list):
            self.response_js = self.response_js[0]
        self.response_js=safe_json_loads(self.response_js)
        return self.recent_file,self.response_js
    def get_response_bools(self):
        response_bool_js = {"abort":json_key_or_default(obj=self.query_js["content"],key="abort",default=False),"additional_response":json_key_or_default(obj=self.query_js["content"],key="additional_response",default=False)}
        for key,value in response_bool_js.items():
            if isinstance(value,str):
               response_bool_js[key]=eatAll(value,['\n','\t',' ',''])
            response_bool_js[key]=make_bool(response_bool_js[key])
        return response_bool_js['abort'],response_bool_js['additional_response'],json_key_or_default(obj=self.query_js["content"],key="notation",default=None)

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
    for file in get_files(directory):
        base_name = os.path.basename(file)
        file_name,ext=os.path.splitext(base_name)
        if ext==".json":
            json_files.append((get_file_create_time(file), file))
    sorted_json_files = sorted(json_files, key=lambda x: x[0])
    aggregated_conversations = []
    chat_log_file = get_open(file_path="chat_log.txt", instance="w")
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
