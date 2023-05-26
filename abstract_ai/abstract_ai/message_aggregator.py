import os
import json
from datetime import datetime
import PySimpleGUI
from functions import *
from simle_gui_templates import *
import PySimpleGUI as sg
from datetime import datetime
def get_timestamp(date_str, military_time_str):
    date_time_str = f"{date_str} {military_time_str}"
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    timestamp = int(date_time_obj.timestamp())
    return timestamp
def file_creation_time(file_path):
    creation_timestamp = os.path.getctime(file_path)
    return creation_timestamp
def find_keys(data, target_keys):
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
    print(st)
    return st
def aggregate_conversations(directory):
    json_files,lsAll = [],[]
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file = os.path.join(root, file)
                json_files.append((file_creation_time(file),file))
    sorted_json_files = sorted(json_files, key=lambda x: x[0])
    aggregated_conversations = []
    chat_log_file = open("chat_log.txt", "w")
    model='gpt'
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
                        lsAll.append({print_it("user"):print_it(value["prompt"])})
                    if 'content' in value:
                        lsAll.append({print_it(model):print_it(value['content'])})
                print(lsAll)
    chat_log_file.close()
    return aggregated_conversations
def browser():
    window = sg.Window('directory_browser',[[sg.Input('',key="selection"),sg.FolderBrowse("Select File", key="-FOLDER_SELECT-", initial_folder="/home/bigrugz/Documents", target="-FOLDER_SELECT-", enable_events=True), sg.Button("select", key="-GRAB_FILE-", enable_events=True), sg.Button("EXIT", key="-EXIT-")]], resizable=True, finalize=True)
    while True:
        event,values = window.read()
        if event == '-GRAB_FILE-':
            window.close()
            break
    return values["selection"]
def get_responses():
    if "response_data" not in os.listdir(os.getcwd()):
        aggregate_conversations(browser())
    else:
        aggregate_conversations("response_data")
