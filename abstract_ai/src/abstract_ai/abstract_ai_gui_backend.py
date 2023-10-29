import os
import re
"""
abstract_ai module
-------------------

The `abstract_ai` module provides a comprehensive class management system to interact with 
the GPT model in an abstracted and structured manner. This module brings together various
sub-modules and components to streamline the process of querying, interpreting, and managing
responses from the GPT model.

Main Components:
- GptManager: The central class managing the interactions and flow between various components.
- ApiManager: Manages the OpenAI API keys and headers.
- ModelManager: Manages model selection and querying.
- PromptManager: Handles the generation and management of prompts.
- InstructionManager: Encapsulates instructions for the GPT model.
- ResponseManager: Manages the responses received from the model.

Dependencies:
- abstract_webtools: Contains tools for handling web-related tasks.
- abstract_gui: GUI related tools and components.
- abstract_utilities: Utility functions and classes for general operations.
- abstract_ai_gui_layout: Defines the general layout for the AI GUI.

Usage:
1. Initialize the GptManager class.
2. Use the update methods to set or change configurations.
3. Use `get_query()` to query the GPT model and retrieve a response.

Author: putkoff
Date: 05/31/2023
Version: 1.0.0
"""
import sys
import openai
import pyperclip
from abstract_webtools import UserAgentManager,UrlManager,SafeRequest,url_grabber_component
from abstract_gui import get_event_key_js,make_component,expandable,AbstractBrowser,text_to_key,NextReadManager, AbstractWindowManager
from . import ApiManager,ModelManager,PromptManager,InstructionManager,ResponseManager
from abstract_utilities import get_any_key,find_paths_to_key,find_keys,unified_json_loader,get_sleep,eatAll,safe_json_loads,read_from_file,make_list,ThreadManager,HistoryManager
from .abstract_ai_gui_layout import get_total_layout
class GptManager:
    def __init__(self):
        self.window_mgr = AbstractWindowManager()
        self.window_name = self.window_mgr.add_window(window_name="Chat GPT Console", layout=get_total_layout(),**expandable())
        self.window_mgr.set_current_window(self.window_name)
        self.window = self.window_mgr.current_window
        self.values = None
        self.event = None
        self.chunk_title=None
        self.browser_mgr = AbstractBrowser(window_mgr=self)
        self.next_read_mgr=NextReadManager()
        self.thread_mgr = ThreadManager()
        self.history_mgr = HistoryManager()
        self.model_mgr = ModelManager()
        self.instruction_mgr = InstructionManager()
        self.chunk_history_name = self.history_mgr.add_history_name('chunk')
        self.response=False
        self.updated_progress = False
        self.test_bool=False
        self.min_chunk = 0
        self.max_chunk=0
        self.initialize_keys()
        self.initialized=False
        self.loop_one=False
    def initialize_keys(self):
        self.toke_percentage_dropdowns = ['-COMPLETION_PERCENTAGE-','-PROMPT_PERCENTAGE-']
        self.additions_key_list = ["-FILES_BROWSER-","-DIR-","-DIRECTORY_BROWSER-","-FILES_LIST-","-SCAN_MODE_ALL-","-SELECT_HIGHLIGHTED-","-SCAN-", "-MODE-", "-BROWSE_BACKWARDS-", "-BROWSE_FORWARDS-",'-FILE_TEXT-','-ADD_FILE_TO_CHUNK-']
        self.instruction_pre_keys = ["additional_responses","suggestions","abort","additional_instruction","notation","instruction","generate_title"]
        self.instruction_keys = self.get_bool_and_text_keys(self.instruction_pre_keys,['TEXT','BOOL'])
        self.sectioned_chunk_text_number_key= text_to_key('chunk text number')
        self.sectioned_chunk_data_key = text_to_key('chunk sectioned data')
        self.chunk_select_keys=self.get_bool_and_text_keys(["chunk text back",'chunk text number',"chunk text forward"])
        self.chunk_display_keys=self.get_bool_and_text_keys(['completion tokens available','completion tokens desired','completion tokens used','prompt tokens available','prompt tokens desired','prompt tokens used','chunk sectioned data','chunk length','chunk total'])
        self.prompt_keys = self.get_bool_and_text_keys(['role','completion_percentage','prompt_data','request','prompt','prompt_data']+self.toke_percentage_dropdowns)+self.chunk_select_keys
    def update_model_mgr(self):
        self.model_mgr = ModelManager(input_model_name=self.window_mgr.get_from_value(text_to_key('model')))
        self.window_mgr.update_value(text_to_key('model'),self.model_mgr.selected_model_name)
        self.window_mgr.update_value(text_to_key('endpoint'),self.model_mgr.selected_endpoint)
        self.window_mgr.update_value(text_to_key('max_tokens'),self.model_mgr.selected_max_tokens)
        print("model_mgr updated...")
    def update_instruct_keys(self):
        values=[]
        for i,each in enumerate(self.instruction_keys[:-6]):
            bool_done = False
            if "TEXT" in each:
                text_value = self.window_mgr.get_from_value(each)
                value = True if text_value == '' else text_value
            elif "BOOL" in each:
                bool_done = True
                bool_value  = self.window_mgr.get_from_value(each)
                value =bool_value if bool_value == False else value
            if bool_done:
                values.append(value)
        return values
    def update_instruction_mgr(self):
        self.additional_responses,self.suggestions,self.abort,self.additional_instruction,self.notation =self.update_instruct_keys()
        self.generate_title=self.window_mgr.get_from_value(self.instruction_keys[-1])
        self.instruction_mgr = InstructionManager(notation=self.notation,suggestions=self.suggestions,abort=self.abort,generate_title=self.generate_title,additional_responses=self.additional_responses,additional_instruction=self.additional_instruction)
        self.update_bool_and_text_values([[self.instruction_mgr.additional_responses,"additional_responses"],[self.instruction_mgr.suggestions,"suggestions"],[self.instruction_mgr.abort,"abort"],[self.additional_instruction,"additional_instruction"],[self.instruction_mgr.notation,"notation"]])
        self.window_mgr.update_value(text_to_key("instruction"),self.instruction_mgr.instructions)
        print("instruction_mgr updated...")
    def update_api_mgr(self):
            self.content_type=self.window_mgr.get_from_value(text_to_key("content_type"),delim='')
            self.header=self.window_mgr.get_from_value(text_to_key("header"),delim='')
            self.api_env=self.window_mgr.get_from_value(text_to_key("api_env"),delim='')
            self.api_key=self.window_mgr.get_from_value(text_to_key("api_key"),delim='')
            self.api_mgr = ApiManager(content_type=self.content_type,header=self.header,api_env=self.api_env,api_key=self.api_key)
            print("api_mgr updated...")
    def update_prompt_mgr(self,prompt_data=None,token_dist=None,completion_percentage=None,bot_notation=None,chunk=None,chunk_type='TEXT'):
        print('updating prompt mgr...')
        self.role=self.window_mgr.get_from_value('-ROLE-')
        if completion_percentage == None:
            completion_percentage=self.window_mgr.get_from_value('-COMPLETION_PERCENTAGE-')
        self.completion_percentage=completion_percentage
        if prompt_data == None:
            prompt_data = self.window_mgr.get_from_value('-PROMPT_DATA-')
        self.prompt_data=prompt_data
        self.chunk_type=chunk_type
        self.request=self.window_mgr.get_from_value(text_to_key('request'))
        self.token_dist=token_dist
        self.bot_notation=bot_notation
        self.chunk=chunk
        self.prompt_mgr = PromptManager(instruction_mgr=self.instruction_mgr,
                                   model_mgr=self.model_mgr,
                                   role=self.role,
                                   completion_percentage=self.completion_percentage,
                                   prompt_data=self.prompt_data,
                                   request=self.request,
                                   token_dist=self.token_dist,
                                   bot_notation=self.bot_notation,
                                   chunk=self.chunk,
                                   chunk_type='TEXT')
        
        if self.token_dist:
            self.max_chunk = int(self.token_dist[0]["chunk"]["total"])-1
        self.chunk_number = min(int(self.window_mgr.get_from_value(self.sectioned_chunk_text_number_key)),self.max_chunk)
        self.window_mgr.update_value('-PROMPT-',self.prompt_mgr.create_prompt(self.chunk_number))
        self.token_dist = self.prompt_mgr.token_dist
        if self.chunk_number > self.max_chunk:
            self.chunk_number = self.max_chunk
        self.update_chunk_info()
        print("prompt_mgr updated...")
    def update_response_mgr(self):
        self.response_mgr = ResponseManager(prompt_mgr=self.prompt_mgr,api_mgr=self.api_mgr)
        print("response_mgr updated...")
    def get_query(self):
        self.response
        while not self.response_mgr.query_done:
            if self.response:
                self.thread_mgr.stop('api_call')
            self.response = self.response_mgr.initial_query()
            if self.response_mgr.query_done:
                print('Response Recieved')
        self.thread_mgr.stop('api_call',result=self.response)
    def update_all(self):
        self.update_model_mgr()
        self.update_instruction_mgr()
        self.update_api_mgr()
        self.update_prompt_mgr()
        self.update_response_mgr()
        self.check_test_bool()
    def is_code(self,text):
        patterns = [
            r'\w+\(\w*\)',           # function calls e.g., func(), hello(arg)
            r'[\w_]+\s*=\s*[\w_]+',  # variable assignments e.g., x = 1
            r'for\s+\w+\s+in',       # loops e.g., for x in ...
            r'if\s+\w+',             # if statements e.g., if x
        ]
        for pattern in patterns:
            try:
                result = re.search(pattern, text)
                return result
            except:
                pass
        return False
    def get_remainder(self,key):
        return 100-int(self.window_mgr.get_values()[key])
    def check_test_bool(self):
        if self.window_mgr.get_values():
            self.test_bool=self.window_mgr.get_values()['-TEST_RUN-']
            if self.test_bool:
                self.window_mgr.update_value('-PROGRESS_TEXT-', 'TESTING')
                if self.window_mgr.get_values()['-TEST_FILE-']:
                    self.test_bool=os.path.isfile(self.window_mgr.get_values()['-TEST_FILE-'])
            else:
                self.window_mgr.update_value('-PROGRESS_TEXT-', 'Awaiting Prompt')
    def get_new_line(self,num=1):
        new_line = ''
        for i in range(num):
            new_line +='\n'
        return new_line
    def update_feedback(self,key):
        value_key = text_to_key(key,section='feedback')
        content = get_any_key(self.last_response_content,key)
        if content:
            if value_key in self.window_mgr.get_values():
                self.window_mgr.update_value(value_key,content)
            else:
                if content != None:
                    self.append_output(text_to_key(text='other',section='feedback'),f"{key}: {content}"+'\n')
    def update_text_with_responses(self):
        self.last_response_file = self.response_mgr.save_manager.file_path
        self.response = safe_json_loads(unified_json_loader(self.last_response_file))
        self.last_response_content = safe_json_loads(find_keys(self.response,'content'))
        if self.last_response_content:
            if isinstance(self.last_response_content,list):
                self.last_response_content=safe_json_loads(self.last_response_content[0])
        self.last_directory=os.path.dirname(self.last_response_file)
        self.window_mgr.update_value('-DIR_RESPONSES-',self.last_directory)
        self.window["-DIRECTORY_BROWSER_RESPONSES-"].InitialFolder=self.last_directory
        self.window["-FILE_BROWSER_RESPONSES-"].InitialFolder=self.last_directory
        response = safe_json_loads(self.last_response_content)
        title = self.response_mgr.save_manager.title
        self.window_mgr.update_value(text_to_key('title input'),title)
        self.window_mgr.update_value(text_to_key('notation',section='feedback'),self.bot_notation)
        for pre_key in self.instruction_pre_keys:
            self.update_feedback(pre_key)
        if isinstance(response,dict): 
            self.append_output('-RESPONSE-',f"#TITLE#{self.get_new_line(1)}{title}{self.get_new_line(2)}#USER QUERY#{self.get_new_line(1)}{self.request}{self.get_new_line(2)}#{self.model_mgr.selected_model_name} RESPONSE#{self.get_new_line(2)}{response['api_response']}{self.get_new_line(2)}")
            print('response:\n',response)
            print('instruction pre keys:\n',self.instruction_pre_keys)
            for key in response.keys():
                if key not in self.instruction_pre_keys:
                    gui_key = text_to_key(text=key,section='feedback')
                    print(gui_key)
                    if gui_key in self.window_mgr.get_values().keys():
                        self.window_mgr.update_value(gui_key,text_to_key(text=key,section='feedback'))
                    elif key not in ['api_response','generate_title']:
                        self.window[text_to_key(text='other',section='feedback')].update(visible=True)
                        self.append_output(text_to_key(text='other',section='feedback'),f"{key}: {response[key]}"+'\n')
        else:
            self.append_output('-RESPONSE-',str(response))
    def get_bool_and_text_keys(self,key_list,sections_list=[]):
        keys = []
        for text in key_list:
            keys.append(text_to_key(text))
            for section in sections_list:
                keys.append(text_to_key(text,section=section))
        return keys
    @staticmethod
    def text_to_key(text,section=None):
        return text_to_key(text,section=section)
    def get_bool_and_text_values(self,text):
        bool_value=self.window_mgr.get_from_value(text_to_key(text,section='BOOL'))
        if bool_value == False:
            return False
        text_value=self.window_mgr.get_from_value(text_to_key(text,section='TEXT'),default=True,delim='')
        return text_value
    def update_bool_and_text_values(self,update_list):
        for component in update_list:
            text = component[1]
            bool_key=text_to_key(text,section='BOOL')
            text_key = text_to_key(text,section='TEXT')
            self.window_mgr.update_value(bool_key,component[0])
            if text in self.instruction_mgr.instructions_js:
                self.window_mgr.update_value(text_key,self.instruction_mgr.instructions_js[text])
    def get_dots(self):
        count = 0
        stop = False
        dots = ''
        for each in self.dots:
            if each == ' ' and stop == False:
                dots+='.'
                stop = True
            else:
                dots+=each
        self.dots = dots
        if stop == False:
            self.dots = '   '
        get_sleep(1)
        status='Testing'
        if self.test_bool == False:
            status = "Updating Content" if not self.updated_progress else "Sending"
        self.window_mgr.update_value('-PROGRESS_TEXT-', f'{status}{self.dots}')
    def update_progress_chunks(self,done=False):
        chunk = int(self.token_dist[0]['chunk']['total'])
        i_query = int(self.response_mgr.i_query)
        if done == True:
            self.window['-PROGRESS-'].update_bar(100, 100)
            self.window_mgr.update_value('-QUERY_COUNT-', f"a total of {chunk} chunks have been sent")
            self.window_mgr.update_value('-PROGRESS_TEXT-', 'SENT')
            self.updated_progress = True
        else:
            self.get_dots()
            self.window['-PROGRESS-'].update_bar(min(i_query,1), min(chunk,2))
            self.window_mgr.update_value('-QUERY_COUNT-', f"chunk {min(i_query,1)} of {min(chunk,1)} being sent")
    def submit_query(self):
        self.window["-SUBMIT_QUERY-"].update(disabled=True)
        self.dots = '...'
        start_query=False
        while self.response_mgr.query_done == False or start_query == False:
            self.update_progress_chunks()
            if not self.updated_progress:
                
                self.update_all()
                if self.test_bool == False:
                    self.thread_mgr.add_thread(name='api_call',target_function=self.get_query)
                    self.thread_mgr.start('api_call')
                else:
                    
                    self.response = self.response_mgr.initial_query(test=self.test_bool)
                start_query=True    
                self.updated_progress = True
        self.last_output=self.thread_mgr.get_last_result('api_call')
        self.update_progress_chunks(done=True)
        self.update_text_with_responses()
        self.window["-SUBMIT_QUERY-"].update(disabled=False)
        if not self.window_mgr.get_values()['-REUSE_CHUNK-']:
            self.window_mgr.update_value(text_to_key('prompt_data'),'')
    def update_chunk_info(self):
        print(f"chunk updating as {self.token_dist[self.chunk_number]['chunk']['data']}")
        self.window_mgr.update_value(self.sectioned_chunk_data_key, self.token_dist[self.chunk_number]['chunk']['data'])
        self.window_mgr.update_value(self.sectioned_chunk_text_number_key, self.chunk_number)
        self.chunk_dist_section = self.token_dist[self.chunk_number]
        for key in self.chunk_display_keys:
            print(f'updating {key}')
            spl = key[1:-1].lower().split('_')
            if spl[0] in self.chunk_dist_section:
                if spl[-1] in self.chunk_dist_section[spl[0]]:
                    self.window_mgr.update_value(key,self.chunk_dist_section[spl[0]][spl[-1]])
                    print(f'{key} updated')
                else:
                    print(f'{key} not updated')
            else:
                print(f'{key} not found')
    def chunk_navigation(self):
        if self.event in self.chunk_select_keys:
            if self.event == '-CHUNK_TEXT_FORWARD-':
                if self.chunk_number < len(self.token_dist)-1:
                    self.chunk_number += 1
                    self.update_chunk_info()
            elif self.event == '-CHUNK_TEXT_BACK-':
                if self.chunk_number > 0:
                    self.chunk_number -= 1
                    self.update_chunk_info()
    def append_output(self,key,new_content):
        self.window_mgr.update_value(key,self.window_mgr.get_from_value(key)+'\n\n'+new_content)
    def add_to_chunk(self,content):
        if self.window_mgr.get_from_value('-AUTO_CHUNK_TITLE-'):
            if self.chunk_title:
                content="# SOURCE #\n"+self.chunk_title+'\n# CONTENT #\n'+content
        if self.window_mgr.get_from_value('-APPEND_CHUNK-'):
            content = self.window_mgr.get_from_value('-PROMPT_DATA-')+'\n\n'+content
        self.window_mgr.update_value('-PROMPT_DATA-',eatAll(content,['\n']))
        self.history_mgr.add_to_history(name=self.chunk_history_name,data=content)
        return content
    def clear_chunks(self):
        content = ''
        self.window_mgr.update_value('-PROMPT_DATA-',content)
        self.history_mgr.add_to_history(name=self.chunk_history_name,data=content)
        return content
    def get_url(self):
        url = self.window_mgr.get_values()['-URL-']
        if url==None:
            url_list =self.window_mgr.get_values()['-URL_LIST-']
            url = safe_list_return(url_list)
        return url
    def get_url_manager(self,url=None):
        url = url or self.get_url()
        url_manager = UrlManager(url=url)    
        return url_manager
    def while_window(self):
        self.event,self.values=self.window_mgr.read_window()
        self.update_all()
        while True:
            if self.loop_one == True and self.initialized==False:
                self.update_all()
                self.initialized=True
            if self.loop_one == True:
                self.event,self.values=self.window_mgr.read_window()
            self.next_read_mgr.execute_queue()
            self.script_event_js = get_event_key_js(event = self.event,key_list=self.additions_key_list )
            print(self.event)
            if self.event in self.instruction_keys:
                self.update_instruction_mgr()
                self.update_prompt_mgr()
            elif self.event in ['-CLEAR_CHUNKS-','-UNDO_CHUNKS-','-REDO_CHUNKS-','-ADD_URL_TO_CHUNK-','-ADD_FILE_TO_CHUNK-','-ADD_FILE_TO_CHUNK_FILES-','-COMPLETION_PERCENTAGE-','-PROMPT_PERCENTAGE-']:
                data=None
                completion_percentage=None
                if self.event == '-CLEAR_CHUNKS-':
                    data = self.clear_chunks()
                elif self.event in self.toke_percentage_dropdowns:
                    data = self.window_mgr.get_from_value('-PROMPT_DATA-')
                    other_percentage = self.get_remainder(self.event)
                    remainder_key = if_key_return_other(self.event,self.toke_percentage_dropdowns)
                    self.window_mgr.update_value(remainder_key,other_percentage)
                elif self.event == '-UNDO_CHUNKS-':
                    data = self.history_mgr.undo(self.chunk_history_name)
                    self.window_mgr.update_value('-PROMPT_DATA-',data)
                elif self.event == '-REDO_CHUNKS-':
                    data = self.history_mgr.redo(self.chunk_history_name)
                    self.window_mgr.update_value('-PROMPT_DATA-',data)
                elif self.event == '-ADD_URL_TO_CHUNK-':
                    self.chunk_title=self.window_mgr.get_values()[text_to_key('-CHUNK_TITLE-',section='url')]
                    data = self.add_to_chunk(self.window_mgr.get_values()['-URL_TEXT-'])
                    self.chunk_type='URL'
                elif self.script_event_js['found']=='-ADD_FILE_TO_CHUNK-':
                    self.chunk_title=self.window_mgr.get_values()[text_to_key('-CHUNK_TITLE-',section='files')]
                    data = self.add_to_chunk(self.window_mgr.get_values()[self.script_event_js['-FILE_TEXT-']])
                self.update_prompt_mgr(prompt_data=data,completion_percentage=completion_percentage)
            elif self.event == 'Copy Response':
                active_tab_key = self.window_mgr.get_values()['-TABS-']  # get active tab key
                # Construct the key for multiline text box
                multiline_key = active_tab_key.replace('TAB','TEXT')
                if multiline_key in self.window_mgr.get_values():
                    text_to_copy = self.window_mgr.get_values()[multiline_key]
                    pyperclip.copy(text_to_copy)
            elif self.event == '-THEME_CHANGE-':
                sg.theme(self.window_mgr.get_values()['-THEME_LIST-'][0]) 
            elif self.event in "-MODEL-":
                self.update_model_mgr()
            elif self.event in [text_to_key("chunk text forward"),text_to_key("chunk text back")]:
                self.chunk_navigation()
            elif self.script_event_js['found']=='-FILES_LIST-':
                file_path = self.window_mgr.get_values()[self.script_event_js['-DIR-']]
                files_list = self.window_mgr.get_values()[self.script_event_js['-FILES_LIST-']]
                if not os.path.isfile(file_path) and files_list:
                    file_path = os.path.join(file_path,files_list[0])
                    if not os.path.isfile(file_path):
                        self.browser_mgr.handle_event(self.window_mgr.get_values(),self.event,self.window)
                        
                        file_path=None
                if file_path:
                    try:
                        self.window_mgr.update_value(self.script_event_js['-FILE_TEXT-'],safe_json_loads(read_from_file(file_path)))
                        self.chunk_title=os.path.basename(files_list[0])
                        self.window_mgr.update_value(text_to_key('-CHUNK_TITLE-',section='files'),self.chunk_title)
                    except:
                        print(f"cannot read from path {file_path}")
            elif self.event in ['-TEST_RUN-','-TEST_FILE-']:
                self.check_test_bool()
            
            elif self.event == "-SUBMIT_QUERY-":
                self.submit_query()
            elif self.event in ['-GET_SOUP-','-GET_SOURCE_CODE-','-ADD_URL-']:
                url_manager = self.get_url_manager()
                if self.event in ['-GET_SOUP-','-GET_SOURCE_CODE-']:
                    self.chunk_title=None
                    data=self.window_mgr.get_values()['-URL_TEXT-']
                    if url_manager.url:
                        url_list =self.window_mgr.get_values()['-URL_LIST-']
                        if url_list:
                            url = UrlManager(url=self.window_mgr.get_values()['-URL_LIST-'][0]).url
                            self.chunk_title=url
                            self.window_mgr.update_value(text_to_key('-CHUNK_TITLE-',section='url'),url)
                        request_manager = SafeRequest(url_manager=url_manager)
                        if self.event == '-GET_SOURCE_CODE-':
                            self.chunk_type='URL'
                            data = request_manager.source_code
                        elif self.event=='-GET_SOUP-':
                            data = url_grabber_component(url=url)
                            self.chunk_type='SOUP'
                        self.window_mgr.update_value('-URL_TEXT-',data)
                       
                    else:
                        print(f'url {url} is malformed... aborting...')
                elif self.event == '-ADD_URL-':
                    url = url_manager.url
                    url_list = make_list(self.window_mgr.get_values()['-URL_LIST-']) or make_list(url)
                    if url_list:
                        if url not in url_list:
                            url_list.append(url)
                    self.window_mgr.update_value('-URL_LIST-',args={"values":url_list})
            else:
                self.browser_mgr.handle_event(self.window_mgr.get_values(),self.event,self.window)
            self.loop_one=True
        window.close()
