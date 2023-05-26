import PySimpleGUI as sg
import json
import os
from functions import *
from gpt_api_call import *

def ret_globals():
    return globals()

def is_globe(x):
    if x in globals():
        return True
    return False

def change_glob(var:str,val:any,glob:dict=ret_globals())->any:
    glob[var] = val
    return val

def read_window():
    if 'window' in globals():
        return globals()['window'].read()
    return '', {}

def get_value_spec(values,key):
    if key in values:
        return values[key]
    return ''

def get_dir_name():
    return os.path.dirname(os.path.abspath(__file__))

def path_to_local_folder(filename):
    return os.path.join(get_dir_name(), filename)

def write_to_abs_fold(filename, content):
    with open(path_to_local_folder(filename), 'w') as f:
        f.write(content)

def return_prompts():
    keys_dict = {"notation": "place here any notes for you to maintain context of this prompt going into the next",
                 # other key-value pairs ...
                }
    if 'keys_dict' in globals():
        return globals()['keys_dict']
    else:
        return keys_dict

def check_prompt(key:str,value:str):
    return raw_data(return_prompts()["prompt"])

def create_window(title, layout):
    return sg.Window(title, layout, grab_anywhere=False, size=(800, 480), return_keyboard_events=True, finalize=True)

def main():
    window = create_window('Json Editor', return_checks())
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks exit
            break
        if event == 'Check Prompt':
            response = check_prompt(values['new_key'], values['new_value'])
            response = dict_check_conversion(response)
            commentary = response['comment']
            if str(response['revision']).lower() == 'false':
                window['check_result'].update(commentary)
            else:
                title,revision = response['key'],response['prompt']
                if title == 'none':
                    title = values['new_key']
                if revision != 'none':
                    revision_window = create_revision_window(title, revision)
                    rev_event, rev_values = revision_window.read()
                    if rev_event == 'Ok':
                        suggested = ['key','value']
                        for k in range(0,len(suggested)):
                            if rev_values['check_'+suggested[k]] == True:
                                window['new_'+suggested[k]].update(value='suggested_'+suggested[k])
                        revision_window.close()
                    elif rev_event in (sg.WIN_CLOSED, 'Cancel'):
                        revision_window.close()
        if event == 'Save':
            pen(path_to_local_folder('entries.json'),json.dumps(add_js(return_prompts(),{values['new_key']:values['new_value']})))
            sg.Popup('Saved!')
    window.close()

if __name__ == "__main__":
    main()
