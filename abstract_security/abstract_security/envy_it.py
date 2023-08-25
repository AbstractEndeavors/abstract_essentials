#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from abstract_utilities.string_clean import eatAll,eatInner,safe_split
from abstract_utilities.compare_utils import line_contains
from abstract_utilities.type_utils import is_list,is_bool
from abstract_utilities.path_utils import get_slash,path_join,if_not_last_child_join,get_home_folder,simple_path_join,is_file
DEFAULT_FILE_NAME = '.env'
DEFAULT_KEY = 'MY_PASSWORD'
def find_and_read_env_file(file_name:str=DEFAULT_FILE_NAME, key:str=DEFAULT_KEY, start_path:str=None):
    """
    Search for an environment file and read a specific key from it.

    Args:
        file_name (str): Name of the .env file to be searched. Defaults to '.env'.
        key (str): Key to be retrieved from the .env file. Defaults to 'MY_PASSWORD'.
        start_path (str): Directory path to start the search from. If None, search starts from current directory. 

    Returns:
        str: The value corresponding to the key if found, otherwise None.
    """
    # Set the default start_path to the current directory if it's None
    directories = [start_path, os.getcwd(), get_home_folder(), simple_path_join(get_home_folder(),'envy_all')]
    if start_path in [None, os.getcwd()]:
        directories = directories[1:]

    # Try to find the file in the start_path
    for k in range(0,len(directories)):
        env_path = check_env_file(path=directories[k],file_name=file_name)
        if not is_bool(env_path):
            value = search_for_env_key(path=env_path,key=key)
            if value != None:
                return value

def search_for_env_key(path:str,key:str):
    """
    Search for a specific key in a .env file.

    Args:
        path (str): The path to the .env file.
        key (str): The key to search for in the .env file.

    Returns:
        str: The value of the key if found, otherwise None.
    """
    with open(path, "r") as f:
        for line in f:
            eq_split = safe_split(line,['=',0])
            # If the line contains the key, return the value after stripping extra characters
            if line_contains(string=eq_split, compare=key):
                return eatAll(line[len(eq_split):],[' ','','=']).strip()

def check_env_file(path:str,file_name:str=DEFAULT_FILE_NAME):
    """
    Check if the environment file exists in a specified path.

    Args:
        path (str): The path to check for the .env file.
        file_name (str): The name of the .env file. Defaults to '.env'.

    Returns:
        str: The path of the .env file if it exists, otherwise False.
    """
    path = if_not_last_child_join(path=path, child=DEFAULT_FILE_NAME)
    # Return the path if file exists, otherwise return False
    if is_file(path):
        return path
    return False

def safe_env_load(path:str=None):
    """
    Safely load the .env file if it exists at a specified path.

    Args:
        path (str): The path to load the .env file from. If None, no operation is performed. 

    Returns:
        bool: True if the .env file is successfully loaded, otherwise False.
    """
    if path == None:
        return False
    if is_file(path):
        if str(safe_split(path,[get_slash(),-1]))[0] == '.':
            load_dotenv(path)
            return True
    return False

def get_env_value(path:str=None,file_name:str=DEFAULT_FILE_NAME, key:str=DEFAULT_KEY):
    """
    Retrieves the value of the specified environment variable.

    Args:
        path (str): The path to the environment file. Defaults to None.
        file_name (str): The name of the environment file. Defaults to '.env'.
        key (str): The key to search for in the .env file. Defaults to 'MY_PASSWORD'.

    Returns:
        str: The value of the environment variable if found, otherwise None.
    """
    if safe_env_load(path):
        return os.getenv(key)
    return find_and_read_env_file(file_name=file_name, key=key, start_path=os.getcwd())
