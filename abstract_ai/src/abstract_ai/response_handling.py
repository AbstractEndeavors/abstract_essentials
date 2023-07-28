from abstract_utilities.path_utils import path_join, mkdirs,get_file_create_time
from abstract_utilities.time_utils import get_time_stamp,get_date
from abstract_utilities.read_write_utils import write_to_file
from abstract_gui.simple_gui.gui_presets import get_browser
import json
import os
def save_response(js:dict, response:dict, title: str = str(get_time_stamp())):
    """
    Saves the response JSON and generated text to a file.

    Args:
        js (dict): The input JSON dictionary.
        response (dict): The response dictionary.
        title (str, optional): The title for the file. Defaults to the current timestamp.

    Returns:
        str: The generated text.
    """
    generated_text = response.text
    try:
        js['response'] = response.json()
    except:
        print()
    try:
        generated_text = json.loads(js['response']['choices'][0]['message']['content'])
        if 'title' in generated_text:
            title = generated_text['title']
    except:
        print()
    path = mkdirs(path_join(mkdirs(path_join(mkdirs('response_data'), get_date())), js['model']))
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
    input(sorted_json_files)
    aggregated_conversations = []
    chat_log_file = open("chat_log.txt", "w")
    model = 'gpt'
    for file in sorted_json_files:
        input(file)
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
