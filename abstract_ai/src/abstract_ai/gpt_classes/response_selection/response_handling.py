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
from endpoints import get_endpoint_defaults
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
safe_write_to_json(file_path='json.json',data={
    "prompt": {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": "\n                #data chunk#\n\n3\n                #instructions#\n\nyour response is expected to be in JSON format with the keys as follows:\n\n\n0) api_response - place response to prompt here\n1) notation - insert any notes you would like to recieve upon the next chunk distribution in order to maintain context and proper continuity\n2) title - please generate a title for this chat based on the both the context of the query and the context of your response\n\n                #prompt#\n\nplease write a python function that will chatgpt to build a python script from api responses.\n1) the script in data chunk needs to be revised, and converted into a fully functional class function:\n                \n                #current data chunk#\n\ndef get_scan_browser_layout ( ) : `` '' '' Generate the layout for the file/folder scanning window . Returns : -- -- -- -- list : A list of list of PySimpleGUI elements defining the window layout. `` '' '' return [ [ get_gui_fun ( `` Text '' , args= { `` text '' : 'Directory to scan : ' } ) , get_gui_fun ( `` InputText '' , args= { `` default_text '' : os.getcwd ( ) , `` key '' : '-DIR- ' } ) , get_gui_fun ( `` FolderBrowse '' , args= { `` button_text '' : `` Folders '' , `` enable_events '' : True , `` key '' : `` directory '' } ) , get_gui_fun ( `` FileBrowse '' , args= { `` button_text '' : `` Files '' , `` enable_events '' : True , `` key '' : `` files '' } ) ] , [ get_gui_fun ( `` Listbox '' , args= { `` values '' : [ ] , `` size '' : ( 50 , 10 ) , `` key '' : '-FILES- ' , `` enable_events '' : True } ) ] , [ create_row_of_buttons ( { `` button_text '' : `` Scan '' , `` key '' : `` -SCAN- '' , `` enable_events '' : True } , `` < - '' , { `` button_text '' : `` File Scan Mode '' , `` key '' : `` -MODE- '' , `` enable_events '' : True } , `` - > '' , 'Select Highlighted ' , 'Ok ' ) ] ] def browse_update ( window=None , key : str = None , args : dict = { } ) : `` '' '' Update specific elements in the browse window . Parameters : -- -- -- -- -- - window : PySimpleGUI.Window The window to be updated . Default is the global ` browse_window ` . key : str , optional The key of the window element to update . args : dict , optional Arguments to be passed for the update operation. `` '' '' window_mgr.update_values ( window=window , key=key , args=args ) def return_directory ( ) : `` '' '' Return the current directory or parent directory if a file path is provided . Returns : -- -- -- -- str : Directory path. `` '' '' values = window.get_values ( ) directory = values [ '-DIR- ' ] if is_file ( values [ '-DIR- ' ] ) : directory = get_directory ( values [ '-DIR- ' ] ) if directory == `` : directory = os.getcwd ( ) return directory def window_while ( event ) : `` '' '' Event handler function for the file/folder scanning window . Parameters : -- -- -- -- -- - event : str Name of the event triggered in the window. `` '' '' print ( event ) values = window_mgr.get_values ( ) if event == `` files '' : browse_update ( key='-DIR- ' , args= { `` value '' : values [ `` files '' ] } ) if event == `` directory '' : browse_update ( key='-DIR- ' , args= { `` value '' : values [ `` directory '' ] } ) if event == '-SCAN- ' : bridge_mgr [ `` last_scan '' ] = is_file ( values [ '-DIR- ' ] ) scan_results = scan_directory ( return_directory ( ) , bridge_mgr [ `` scan_mode '' ] ) browse_update ( key='-FILES- ' , args= { `` values '' : scan_results } ) if event == 'Select Highlighted ' : if len ( values [ '-FILES- ' ] ) > 0 : browse_update ( key='-DIR- ' , args= { `` value '' : os.path.join ( return_directory ( ) , values [ '-FILES- ' ] [ 0 ] ) } ) if event == '-MODE- ' : bridge_mgr [ `` scan_mode '' ] = 'folder ' if bridge_mgr [ `` scan_mode '' ] == 'file ' else 'file' bridge_mgr [ `` browse_window '' ] .Element ( '-MODE- ' ) .update ( text=f '' F { bridge_mgr [ 'scan_mode ' ] [ 1 : ] } Scan Mode '' ) if event == `` < - '' : # Navigate up to the parent directory if return_directory ( ) not in bridge_mgr [ `` history '' ] : bridge_mgr [ `` history '' ] .append ( return_directory ( ) ) directory = os.path.dirname ( return_directory ( ) ) # This will give the parent directory browse_update ( key='-DIR- ' , args= { `` value '' : directory } ) browse_update ( key='-FILES- ' , args= { `` values '' : scan_directory ( directory , bridge_mgr [ `` scan_mode '' ] ) } ) if event == `` - > '' : # Navigate down into the selected directory or move to the next history path if values [ '-FILES- ' ] : # If there 's a selected folder in the listbox directory = os.path.join ( return_directory ( ) , values [ '-FILES- ' ] [ 0 ] ) forward_dir ( directory ) elif bridge_mgr [ `` history '' ] : # If there 's a directory in the history stack directory = bridge_mgr [ `` history '' ] .pop ( ) browse_update ( key='-DIR- ' , args= { `` value '' : directory } ) browse_update ( key='-FILES- ' , args= { `` values '' : scan_directory ( directory , bridge_mgr [ `` scan_mode '' ] ) } ) def forward_dir ( directory ) : `` '' '' Navigate and update the scanner to display contents of the given directory . Parameters : -- -- -- -- -- - directory : str Path to the directory to navigate to. `` '' '' if os.path.isdir ( directory ) : browse_update ( key='-DIR- ' , args= { `` value '' : directory } ) browse_update ( key='-FILES- ' , args= { `` values '' : scan_directory ( directory , bridge_mgr [ `` scan_mode '' ] ) } ) def scan_directory ( directory_path , mode ) : `` '' '' List files or folders in the given directory based on the provided mode . Parameters : -- -- -- -- -- - directory_path : str Path to the directory to scan . mode : str Either 'file ' or 'folder ' to specify what to list . Returns : -- -- -- -- list : List of file/folder names present in the directory. `` '' '' if mode == 'file ' : return [ f for f in os.listdir ( directory_path ) if os.path.isfile ( os.path.join ( directory_path , f ) ) ] else : # mode == 'folder' return [ d for d in os.listdir ( directory_path ) if os.path.isdir ( os.path.join ( directory_path , d ) ) ] def get_browse_scan ( ) : `` '' '' Initialize and run the file/folder scanner window with default settings . Returns : -- -- -- -- str : The path selected in the scanner. `` '' '' bridge_mgr [ `` scan_mode '' ] = `` file '' bridge_mgr [ `` history '' ] = [ ] return window_mgr.while_basic ( window=bridge_mgr [ `` browse_window '' ] ) [ `` -DIR- '' ] def popup_T_F ( title : str = `` popup window '' , text : str = `` popup window text '' ) : answer = get_yes_no ( title=title , text=text ) if answer == `` Yes '' : return True return False def create_new_entity ( event : str = None , entity_type : str = `` Folder '' ) : # Retrieve values from the GUI values = window_mgr.get_values ( window=window_mgr.get_last_window_method ( ) ) if `` -ENTITY_TYPE- '' in values : entity_type = values [ `` -ENTITY_TYPE- '' ] if event in [ `` -FOLDER_BROWSE- '' , '-ENTITY_NAME- ' ] : if os.path.isfile ( values [ '-ENTITY_NAME- ' ] ) : window_mgr.update_values ( window=window_mgr.get_last_window_method ( ) , key= '' -PARENT_DIR- '' , args= { `` value '' : get_directory ( values [ '-ENTITY_NAME- ' ] ) } ) file_name = get_base_name ( values [ '-ENTITY_NAME- ' ] ) window_mgr.update_values ( window=window_mgr.get_last_window_method ( ) , key='-ENTITY_NAME- ' , args= { `` value '' : file_name } ) if event == `` Create '' : exists = False if values [ '-ENTITY_NAME- ' ] and values [ '-PARENT_DIR- ' ] : entity_path = os.path.join ( values [ '-PARENT_DIR- ' ] , values [ '-ENTITY_NAME- ' ] ) if entity_type == `` Folder '' : exists = os.path.exists ( entity_path ) # changed from os.path.dir_exists ( entity_path ) if entity_type == `` File '' : exists = os.path.exists ( entity_path ) if exists : if not popup_T_F ( title=f '' Override the { entity_type } ? `` , text=f '' looks like the { entity_type } path { entity_path } already exists did you want to overwrite it ? `` ) : return False if entity_type == `` Folder '' and not exists : os.makedirs ( entity_path , exist_ok=True ) elif entity_type == `` File '' : with open ( entity_path , ' w ' ) as f : if `` save_data '' in bridge_mgr : f.write ( bridge_mgr [ ``\n                "
            }
        ],
        "max_tokens": 3276
    },
    "response": {
        "id": "chatcmpl-89Rn51QbJjo0CZsDKudhR0gtq4e0b",
        "object": "chat.completion",
        "created": 1697262471,
        "model": "gpt-4-0613",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "{\n\"api_response\": \"Here is a function named 'FileFolderScanner' that encapsulates all the provided functions into a Python class:\n\n```python\nimport os\nfrom PySimpleGUI import Text, InputText, FolderBrowse, FileBrowse, Window, ListBox\nfrom typing import List\n\n\nclass FileFolderScanner:\n    def __init__(self):\n        self.history = []\n        self.scan_mode = 'file'\n        self.gui_fun = None\n        self.window_mgr = None\n        self.browse_window = None\n        self.bridge_mgr = {}\n\n    def get_scan_browser_layout(self):\n        # your implementation here\n\n    def browse_update(self, window=None, key: str=None , args: dict={}):\n        # your implementation here\n\n    def return_directory(self) -> str:\n        # your implementation here\n\n    def window_while(self, event: str):\n        # your implementation here\n\n    def forward_dir(self, directory):\n        # your implementation here\n\n    def scan_directory(self, directory_path, mode) -> List[str]:\n        # your implementation here\n\n    def get_browse_scan(self) -> str:\n        # your implementation here\n\n    def popup_T_F(self, title: str, text: str) -> bool:\n        # your implementation here\n\n    def create_new_entity(self, event: str=None, entity_type: str=None):\n        # your implementation here\n```\",\n\"notation\": \"The response consists of a Python class named 'FileFolderScanner' which encapsulates all the functions provided in the data chunk. Class functions are converted from the functions given. Function names and parameters remain the same to maintain functionality. User will need to provide implementations for each function and populate self.gui_fun, self.window_mgr, self.browse_window, and self.bridge_mgr as per their needs.\",\n\"title\": \"Converting Python Functions into Class Method Structure\"\n}"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 2076,
            "completion_tokens": 379,
            "total_tokens": 2455
        }
    },
    "content": "{\n\"api_response\": \"Here is a function named 'FileFolderScanner' that encapsulates all the provided functions into a Python class:\n\n```python\nimport os\nfrom PySimpleGUI import Text, InputText, FolderBrowse, FileBrowse, Window, ListBox\nfrom typing import List\n\n\nclass FileFolderScanner:\n    def __init__(self):\n        self.history = []\n        self.scan_mode = 'file'\n        self.gui_fun = None\n        self.window_mgr = None\n        self.browse_window = None\n        self.bridge_mgr = {}\n\n    def get_scan_browser_layout(self):\n        # your implementation here\n\n    def browse_update(self, window=None, key: str=None , args: dict={}):\n        # your implementation here\n\n    def return_directory(self) -> str:\n        # your implementation here\n\n    def window_while(self, event: str):\n        # your implementation here\n\n    def forward_dir(self, directory):\n        # your implementation here\n\n    def scan_directory(self, directory_path, mode) -> List[str]:\n        # your implementation here\n\n    def get_browse_scan(self) -> str:\n        # your implementation here\n\n    def popup_T_F(self, title: str, text: str) -> bool:\n        # your implementation here\n\n    def create_new_entity(self, event: str=None, entity_type: str=None):\n        # your implementation here\n```\",\n\"notation\": \"The response consists of a Python class named 'FileFolderScanner' which encapsulates all the functions provided in the data chunk. Class functions are converted from the functions given. Function names and parameters remain the same to maintain functionality. User will need to provide implementations for each function and populate self.gui_fun, self.window_mgr, self.browse_window, and self.bridge_mgr as per their needs.\",\n\"title\": \"Converting Python Functions into Class Method Structure\"\n}"
})
