from abstract_utilities.path_utils import path_join, mkdirs,get_file_create_time
from abstract_utilities.time_utils import get_time_stamp,get_date
from abstract_utilities.read_write_utils import write_to_file
from abstract_gui import get_browser
import json
import os
def get_unique_title(title:str=str(get_time_stamp()),directory:str=os.getcwd()):
    """
    Generates a unique title by appending an index number to the given base title.

    Args:
        title (str, optional): The base title to start with. Defaults to a timestamp-based string.
        directory (str, optional): The directory to search for existing titles. Defaults to the current working directory.

    Returns:
        A unique title string formed by appending an index number to the base title.
    """
    existing_indices = [int(name.split('_')[-1]) for name in dir_list if name.startswith(title + '_') and name.split('_')[-1].isdigit()]
    next_index = max(existing_indices, default=-1) + 1 if existing_indices else 0
    return title + '_' + str(next_index)
def save_response(prompt_js:dict={},endpoint:str=None response:(dict or str)=None, title:str=None,directory:str=None):
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
        diretocyr = 'response_data'
    if title == None:
        title= str(get_time_stamp())
    if endpoint == None:
        js
    if response == None:
        return {}
    generated_text = response.text
    try:
        js['response'] = response.json()
    except:
        pass
    try:
        generated_text = json.loads(js['response']['choices'][0]['message']['content'])
        if 'title' in generated_text:
            title = generated_text['title']
    except:
        pass
    path = mkdirs(path_join(mkdirs(path_join(mkdirs(directory), get_date())), js['model']))
    create_unique_title(title=title,directory=mkdirs(directory))
    write_to_file(filepath=path_join(path, title + '.json'), contents=json.dumps(js))
    return generated_text
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
def find_value_by_key_path(json_data, key_path):
    """
    Finds the value in a JSON-like structure given a specific key path.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key_path (list): A list of keys representing the path to the desired value.

    Returns:
        The value found at the specified key path, or None if not found.
    """
    def search_in_path(data, keys):
        for key in keys:
            if isinstance(data, dict):
                if key in data:
                    data = data[key]
                else:
                    return find_values_by_key(data, key)
            elif isinstance(data, list):
                try:
                    index = int(key)
                    data = data[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return data

    value = search_in_path(json_data, key_path)
    return value

def find_values_by_key(json_data, key):
    """
    Finds all values in a JSON-like structure associated with a specific key.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key (str): The key to search for.

    Returns:
        A list of dictionaries containing the path of keys leading to each value and the value itself.
    """
    result = []
    def search_in_json(data, keys=[]):
        if isinstance(data, dict):
            if key in data:
                result.append({"keys": keys + [key], "value": data[key]})
            for sub_key, value in data.items():
                search_in_json(value, keys + [sub_key])
        elif isinstance(data, list):
            for index, item in enumerate(data):
                search_in_json(item, keys + [str(index)])
    search_in_json(json_data)
    return result
def find_path_to_key(json_data, key_to_find):
    """
    Finds the path to a specific key within a JSON-like structure.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        key_to_find (str): The key to find the path for.

    Returns:
        A list of keys representing the path to the specified key, or None if the key is not found.
    """
    def search_path(data, current_path=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    return new_path
                found_path = search_path(value, new_path)
                if found_path:
                    return found_path
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                found_path = search_path(item, new_path)
                if found_path:
                    return found_path
        return None

    path = search_path(json_data)
    return path
def find_path_to_value(json_data, value_to_find):
    """
    Finds the path to a specific value within a JSON-like structure.

    Args:
        json_data (dict or list): The JSON-like structure to search in.
        value_to_find: The value to find the path for.

    Returns:
        A list of keys representing the path to the specified value, or None if the value is not found.
    """
    def search_path(data, current_path=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if value == value_to_find:
                    return new_path
                found_path = search_path(value, new_path)
                if found_path:
                    return found_path
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                if item == value_to_find:
                    return new_path
                found_path = search_path(item, new_path)
                if found_path:
                    return found_path
        return None

    path = search_path(json_data)
    return path
def get_response(endpoint:str,endpoint_subsection:str=None,param:(str)="response_key"):
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
    response = find_value_by_key_path(get_endpoint_defaults(),key_path)
    key_path.append(param)
    input(key_path)
    if param == "response_key":
        response_key = find_value_by_key_path(get_endpoint_defaults(),key_path)
        if isinstance(response_key,list):
            if isinstance(response_key[0],dict):
                if "value" in response_key[0]:
                    response_key = response_key[0]["value"]
        response=find_value_by_key_path(response,[response_key])[0]["value"]
    return response
import json
