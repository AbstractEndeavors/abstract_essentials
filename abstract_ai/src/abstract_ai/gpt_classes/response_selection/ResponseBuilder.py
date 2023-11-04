import os
import requests
from abstract_utilities import (get_date,
                                get_time_stamp,
                                mkdirs,
                                get_files,
                                unified_json_loader,
                                safe_json_loads,
                                safe_read_from_json,
                                get_file_create_time,
                                get_highest_value_obj,
                                )
from abstract_utilities.json_utils import get_any_value,safe_json_loads,safe_dump_to_file
class SaveManager:
    """
    Manages the saving of data. This class should provide methods to specify where (e.g., what database or file) and how (e.g., in what format) data should be saved.
    """
    def __init__(self, data,title=None,directory=None,model='default'):
        self.data = safe_json_loads(data)
        self.model=model
        self.date = get_date()
        self.directory = mkdirs(directory or os.path.join(os.getcwd(), 'response_data'))
        self.directory = mkdirs(os.path.join(self.directory, self.date))
        self.directory = mkdirs(os.path.join(self.directory), self.model)
        self.file_name = self.create_unique_file_name()
        self.file_path = os.path.join(self.directory, self.file_name)
        self.save_data_to_file()

    def create_unique_file_name(self):
        base_name = f"{self.title}.json"
        index = 1
        unique_name = base_name
        while os.path.exists(os.path.join(self.directory, unique_name)):
            unique_name = f"{self.title}_{index}.json"
            index += 1
        return unique_name
    def determine_folder(self):
        unlist_it(self,['directory','date','model'])
        if get_any_value(self.content,'error'):
            self.error=True
            self.fold_model= mkdirs(os.path.join(self.directory,self.date,'error'))
        else:
            self.fold_model= mkdirs(os.path.join(self.directory,self.date,self.model))
    def create_unique_name(self):
        self.title = self.create_unique_title(title=self.original_title,directory=self.fold_model)
        self.query_js["title"]=self.title
        self.file_name = f'{self.title}.json'
    def save_file(self):
        self.file_path = os.path.join(self.fold_model,self.file_name)
        self.query_js["file_path"]=self.file_path
        safe_dump_to_file(file_path=self.file_path,data=str(self.query_js))
    def save_data_to_file(self):
        with open(self.file_path, 'w') as file:
            file.write(self.data)

class ResponseManager:
    """
    The `ResponseManager` class handles the communication process with AI models by managing the sending of queries and storage of responses. It ensures that responses are correctly interpreted, errors are managed, and that responses are saved in a structured way, facilitating easy retrieval and analysis.

    It leverages various utilities from the `abstract_utilities` module for processing and organizing the data and interacts closely with the `SaveManager` for persisting responses.

    Attributes:
        prompt_mgr (Any): An instance of the prompt manager that is responsible for creating the prompts that will be sent to the AI model.
        api_mgr (Any): An instance that manages the communication with the API endpoint for sending queries and receiving responses.
        title (str, optional): The title for the session or the saved file. Defaults to None.
        directory (str, optional): The path to the directory where responses will be saved. Defaults to the 'response_data' folder in the current working directory.
        bot_notation (Any, optional): A notation used by the bot for managing responses. Defaults to None.
        token_dist (List[Any]): A list that contains information about the distribution of tokens or elements related to the response.
        output (List[Any]): A list to store output data after processing.
        content (Dict[Any, Any]): A dictionary to hold the content of the response.
        query_js (Dict[Any, Any]): A dictionary that holds the complete query and response data.
        chunk_descriptions (List[str]): A list to hold descriptions of different chunks of the response if applicable.
        i_query (int): An index to keep track of the query being processed.
        original_title (str): The original title for the session or saved file.
        query_done (bool): A flag to indicate if the query process is complete.
        response_keys (List[str]): A list of keys that are expected or relevant in the responses.

    Methods:
        re_initialize_query: Resets query-related attributes to their default state for a new query cycle.
        post_request: Sends a POST request with the current prompt and headers to the AI model and handles the response.
        get_response: Extracts and formats the response from the API call.
        try_load_response: Attempts to load the response content into a structured format.
        extract_response: Processes the response and manages the creation of a save point through `SaveManager`.
        get_last_response: Retrieves the last response from the save location.
        get_response_bools: Checks and sets boolean flags based on the content of the latest response.
        send_query: Prepares and sends a new query to the AI model, then processes the response.
        test_query: Simulates sending a query for testing purposes.
        prepare_response: Handles the response after a query has been sent.
        initial_query: Manages the initial sequence of sending queries and processing responses.

    """

    def __init__(self,prompt_mgr,api_mgr,title=None,directory=None):
        self.prompt_mgr=prompt_mgr
        self.model_mgr=self.prompt_mgr.model_mgr
        self.api_mgr=api_mgr
        self.title=title
        self.directory=mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        self.token_dist=prompt_mgr.token_dist
        self.output=[]
        self.content={}
        self.query_js={}
        self.bool_test=False
        self.chunk_descriptions=[]
        self.i_query=0
        self.original_title=self.title
        self.query_done=False
        self.re_initialize_query()
    def re_initialize_query(self):
        self.query_done=False
        self.i_query = 0
        self.abort_js = {"abort":None,"additional_responses":None,"request_chunks":None}
        self.response_keys = ["abort","additional_responses","suggestions","notation","generate_title","request_chunks","api_response","token_adjustment","prompt_as_previous"]
        self.original_title=None
        self.suggestions=False
        self.notation=False
        self.api_response={}
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
        """
        Attempts to load the response content into a structured format.
        """
        self.api_response = safe_json_loads(self.get_response())
    def extract_response(self):
        """
        Processes the response and manages the creation of a save point through `SaveManager`.
        """
        return self.query_js
    def get_last_response(self):
        """
        Retrieves the last response from the save location.

        Returns:
            tuple: A tuple containing the file path and the response dictionary.
        """
        self.recent_file = get_highest_value_obj(get_files(self.directory),function=get_file_create_time)
        self.last_response = safe_json_loads(safe_read_from_json(self.recent_file))
        self.content = safe_json_loads(get_any_value(self.api_response,'content'))
        self.response_js= safe_json_loads(get_any_value(self.content, 'api_response'))
        return self.recent_file,self.response_js
    def get_abort():
       self.abort_js = {"abort":None,"additional_responses":None,"request_chunks":None}
       for key,value in self.prompt_mgr.instructions_js.items():
           if key in list(self.abort_js.keys()):
              setattr(self,key,value)
              self.abort_js[key]=value
           if self.abort_js["abort"]:
               return True
       if self.abort_js["request_chunks"] or self.abort_js["additional_responses"]:
           return False
       else:
           return True
    def send_query(self):
        """
        Handles the response after a query has been sent.
        """
        self.prompt = self.prompt_mgr.create_prompt(dist_number=self.i_query, bot_notation=self.notation,generate_title=self.generate_title,request_chunks=self.request_chunks,token_adjustment=self.token_adjustment,prompt_as_previous=self.prompt_as_previous)
        self.endpoint = self.model_mgr.selected_endpoint
        self.header = self.api_mgr.header
        self.response = requests.post(url=self.endpoint, json=self.prompt, headers=self.header)
        self.try_load_response()
        self.api_response = safe_json_loads(get_reg_response())
        self.query_js={}
        self.content = get_any_value(self.api_response,'content')
        if self.content and isinstance(self.content,list):
            if len(self.content)>0:
                self.content = safe_json_loads(self.content[0])
        self.content["request_chunks"]=True
        self.query_js["prompt"]=safe_json_loads(self.prompt)
        self.query_js["response"] = safe_json_loads(self.api_response)
        self.query_js["query_response"]=self.content
        self.model= get_any_value(self.query_js["response"],'model') or get_any_value(self.query_js["response"],'error') or 'default' 
        self.title = self.original_title or  self.get_any_value(self.content,'generate_title') or get_any_value(self.query_js["response"],'created')
        self.save_manager = SaveManager(data=self.query_js,title=self.title,directory=self.directory,model=self.model)
        self.query_js['file_path']=save_manager.file_path
        self.output.append(self.query_js)
        for i,key in enumerate(self.response_keys):
            setattr(self,key,get_any_value(self.content,key))
    def initial_query(self):
        """
        Manages the initial sequence of sending queries and processing responses.

        Returns:
            list: List of output data after processing.
        """
        self.query_done=False
        self.i_query = 0
        for i in range(len(self.token_dist)):
            response_loop=True
            abort_it=False
            while response_loop:
                self.send_query()
                if self.get_abort() or self.abort_js["abort"]:
                    response_loop=False
                    break
            print(f'in while {i}')
            if self.abort_js["abort"]:
                break
            self.i_query=i
        self.query_done=True
        self.i_query=0
        return self.output
