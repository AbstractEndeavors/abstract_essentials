import os
import json
from datetime import datetime
import PySimpleGUI
from functions import *
from simple_gui_templates import *
import PySimpleGUI as sg


def get_timestamp(date_str, military_time_str):
    """
    Converts a date string and military time string to a timestamp.

    Args:
        date_str (str): The date string in the format 'YYYY-MM-DD'.
        military_time_str (str): The military time string in the format 'HH:MM'.

    Returns:
        int: The timestamp corresponding to the date and time.
    """
    date_time_str = f"{date_str} {military_time_str}"
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    timestamp = int(date_time_obj.timestamp())
    return timestamp


def file_creation_time(file_path):
    """
    Retrieves the creation timestamp of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        float: The creation timestamp of the file.
    """
    creation_timestamp = os.path.getctime(file_path)
    return creation_timestamp


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


def print_it(st):
    """
    Prints the input string and returns it.

    Args:
        st (str): The string to be printed.

    Returns:
        str: The input string.
    """
    print(st)
    return st


def aggregate_conversations(directory):
    """
    Aggregates conversations from JSON files in the specified directory.

    Args:
        directory (str): The directory containing the JSON files.

    Returns:
        list: A list of aggregated conversations.
    """
    json_files, lsAll = [], []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file = os.path.join(root, file)
                json_files.append((file_creation_time(file), file))
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


def browser():
    """
    Displays a directory browser window and returns the selected directory.

    Returns:
        str: The selected directory.
    """
    window = sg.Window('directory_browser', [
        [sg.Input('', key="selection"), sg.FolderBrowse("Select File", key="-FOLDER_SELECT-", initial_folder="/home/bigrugz/Documents", target="-FOLDER_SELECT-", enable_events=True), 
        sg.Button("select", key="-GRAB_FILE-", enable_events=True), sg.Button("EXIT", key="-EXIT-")]], resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == '-GRAB_FILE-':
            window.close()
            break
    return values["selection"]


def get_responses():
    """
    Retrieves the aggregated conversations from JSON files.

    If the 'response_data' directory does not exist in the current working directory, prompts the user to select a directory
    containing the JSON files. Otherwise, uses the 'response_data' directory.

    Returns:
        None
    """
    if "response_data" not in os.listdir(os.getcwd()):
        aggregate_conversations(browser())
    else:
        aggregate_conversations("response_data")
