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

from abstract_gui import get_browser
class SaveManager:
    def __init__(self,query_js={},title=None,directory=None):
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
