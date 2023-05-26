import PySimpleGUI as sg
import json
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
  if is_globe('window'):
    return window.read()
  return '', {}
def get_value(window=['',{}]):
  return read_window()[1]
# Load previous entries
def get_json_response():
  return "the following will need to be in json format, your response will be described in the following descriptions:\n"
def assign_keys(st):
  return f"as a value for the '{st}' key: "
def get_key_desc(st,text):
  return f"{assign_keys(st)}{text}\n"
def get_dir_name():
  # Get the directory of the current script
  return os.path.dirname(os.path.abspath(__file__))
def path_to_local_folder(filename):
    # Join the directory with the new filename
    return create_path(get_dir_name(), filename)
def write_to_abs_fold(filename, content):
    pen(path_to_local_folder(filename),content)
def return_prompts():
    keys_dict = {"notation": "place here any notes for you to maintain context of this prompt going into the next",
                 "title": "place here any notes for you to maintain context of this prompt going into the next",
                 "instruction": "should containing a textual description",
                 "inputs": f"key containing a list of command line inputs, with each input represented as an object with 'type' and 'input' keys. For example:\n'str(return_instruction())'\n'",
                 "text": "please respond with text only","bash": "please respond in the form of a bash script",
                 "response": "place your query response here","context": "provide any relevant context or dependencies for the task",
                 "security": "describe any necessary security measures or precautions for the task",
                 "formatting": "provide instructions on how the output data should be formatted",
                 "validation": "describe the validation process or rules for the input data",
                 "error_handling": "describe how the AI should handle potential errors during this task",
                 "revision": """provide revisions according to line number, for example: [{'lines':[20,25],'revision':'this text goes in place of lines [20:25]'},{...}]""",
                 "prompt": f"""the task is to evaluate a prompt and name that will be used in furure queries,{get_json_response()}{get_key_desc("key","change the key string to something more suitable if applicable, if no changes are to be made the value is none")},\n{get_key_desc("needs_revision","where the value is a boolean indicating whether a revision was suggested. The initial value of 'needs_revision' is false.")},\n{get_key_desc("prompt","if revision is True then the revised prompt should be placed here with the default being none")},\n{get_key_desc("comment","where any commentary about the prompt or task should be placed")}"""}
    return change_glob('keys_dict',exists_make_js('entries.json',exists_make_js('prompt_dict_og.json',keys_dict)),globals())
def add_js(js,js2):
  keys = list(js2.keys())
  for k in range(0,len(keys)):
    js[keys[k]] = js2[keys[k]]
  return js
def get_value_spec(values,key):
  if key in values:
    return values[key]
  return ''
def check_prompt(key:str=get_value_spec(get_value(),'new_key'),value:str=get_value_spec(get_value(),'new_value')):
  return_prompts()
  return raw_data(return_prompts()["prompt"])
# Create layout
class WindowManager:
    def __init__(self):
        self.main_window = sg.Window('Json Editor', self.return_checks())
        self.current_window = self.main_window

    def create_revision_window(self, title, revision):
        layout = [
            [sg.T('suggested title: '), sg.Input(title, key='suggested_key'), sg.Checkbox('', default=True, key='check_key')],
            [sg.T('suggested revision: '), sg.Input(revision, key='suggested_value'), sg.Checkbox('', default=True, key='check_value')],
            [sg.T('commentary: '), sg.T('')],
            [sg.Button('Ok'), sg.Button('Cancel')]
        ]
        return sg.Window('Test Window', layout, grab_anywhere=False, size=(800, 480), return_keyboard_events=True, finalize=True)


    def return_checks(self):
        checkbox_chunks = [list(return_prompts().items())[i:i + 6] for i in range(0, len(return_prompts()), 6)]
        checkbox_layout = [[[sg.Checkbox(k, key=k, default=False, tooltip=v)] for k, v in chunk] for chunk in checkbox_chunks]
        return [
            [sg.Column(checkbox_layout[i]) for i in range(len(checkbox_layout))],
            [sg.Frame('Create A New Prompt',[
                [sg.T('New Key')],[sg.InputText(size=(40, 1), key='new_key')],
                [sg.T('New Value')],[sg.Multiline(size=(40, 4), key='new_value')],
                [sg.Button('Check Prompt')],
                [sg.T('', key='check_result')]])],
            [sg.Button('Save'), sg.Button('Exit')]
        ]

    def process_window_events(self):
        while True:
            event, values = self.current_window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            self.handle_event(event, values)

        self.current_window.close()

    def handle_event(self, event, values):
        if self.current_window == self.main_window:
            if event == 'Check Prompt':
                response = check_prompt(values['new_key'], values['new_value'])
                response = dict_check_conversion(response)
                commentary = response['comment']
                if str(response['revision']).lower() == 'false':
                    self.main_window['check_result'].update(commentary)
                else:
                    title, revision = response['key'], response['prompt']
                    if title == 'none':
                        title = values['new_key']
                    if revision != 'none':
                        self.current_window = self.create_revision_window(title, revision)
            if event == 'Save':
                pen(path_to_local_folder('entries.json'), json.dumps(add_js(return_prompts(), {values['new_key']: values['new_value']})))
                sg.Popup('Saved!')
        else:
            if event == 'Ok':
                suggested = ['key', 'value']
                for k in range(0, len(suggested)):
                    if values['check_' + suggested[k]] == True:
                        self.main_window['new_' + suggested[k]].update(value='suggested_' + suggested[k])
                self.current_window = self.main_window

# Usage
manager = WindowManager()
##manager.process_window_events()
