import openai
import json
import os
import subprocess
import requests
import sys
from subprocess import check_output
import PySimpleGUI as sg
from dotenv import load_dotenv
import base64
import io
from PIL import Image
import re

import io



load_dotenv()
def try_url(url):
    try:
    	r = requests.get(url)
    	data = r.text
    	return True
    except:
    	return False

def get_response_types():
    return ['instruction', 'json', 'bash', 'text']
def get_models():
    return {'/v1/chat/completions': ['gpt-4', 'gpt-4-0314', 'gpt-4-32k', 'gpt-4-32k-0314', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0301'],'/v1/completions': ['text-davinci-003', 'text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001'],'/v1/edits': ['text-davinci-edit-001', 'code-davinci-edit-001'],'/v1/audio/transcriptions': ['whisper-1'],'/v1/audio translations': ['whisper-1'],'/v1/fine-tunes': ['davinci', 'curie', 'babbage', 'ada'],'/v1/embeddings': ['text-embedding-ada-002', 'text-search-ada-doc-001'],'/v1/moderations': ['text-moderation-stable', 'text-moderation-latest']}
def get_endpoints():
    return list(get_models().keys())
def getInstruction():
    return {'instruction': ''''Creating a basic react forum requires you to use the create-react-app command line tool. First, install the tool globally to your machine with the command `npm install -g create-react-app`. Then navigate to the folder you want to create the project in, and use the command `create-react-app project-name` to create the project. Next, you'll need to install the required dependencies to build the forum. This can be done with the command `npm install --save react-router react-router-dom` to install the routing library. Finally, you will need to configure the routes and components in the `src/index.js` file.''',
            'inputs': [{'type': 'module', "path": '', 'instruction': 'install react-app global module with npm',
                        "commands":[{"description":"install react-app","command":'npm install -g create-react-app'}]},
                       {'type': 'file',  'path': 'src', 'instruction': 'create the app component for the project','name': 'App.js',
                        'commands': [{'description': 'make directory', "command": 'mkdir {home_folder}/src/',
                                      'user_input': {'description': 'Please provide the folder path where you want to create the project',
                                                     'item': 'folder', 'name': 'home_folder'}},
                                     {'description': 'create the App.js component',
                                      'command': 'echo -e "import { render, screen } from \'@testing-library/react\';test(\'renders learn react link\', () => {render(<App />);const linkElement = screen.getByText(/learn react/i);expect(linkElement).toBeInTheDocument();});" > App.js'}]},
                       {'type': 'module',  'path': 'src','instruction': 'install libraries to build the forum',
                        'commands': [{"description":"install react-router-dom","command":'npm install --save react-router react-router-dom'}]},
                       {'type': 'file', 'path': 'src','instruction': 'configure the routes and components in the index.js file', 'name': 'index.js',
                        'commands': [{'description': 'create the index.js file','command':'echo -e "import React from \'react\';\nimport { render } from \'react-dom\'"'}]}]}
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"Error running command: {error.decode('utf-8')}")
    if output:
        print(output.decode('utf-8'))

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height
    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)
    return image.resize((width, height), Image.ANTIALIAS)
def display_image(window, filepath):
    try:
        image = resize_image(Image.open(filepath), 300, 300)
        #image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-TAB_IMAGE_CONTENT-"].update(data=base64.b64encode(bio.getvalue()).decode("utf-8"))
        return data
    except Exception as e:
        print(f"Error displaying image: {e}")
        return ''
def prePrompt(pre='',types = ''):
    pre = ''
    js = {'json':'please respond in json format','instruction':'The response should have an "instruction" key containing a textual description, and an "inputs" key containing a list of command line inputs, with each input represented as an object with "type" and "input" keys. For example:\n'+str(getInstruction())+'\n','text':"please respond with text only","bash":"please respond in the form of a bash script"}
    if types in js:
        pre = js[types]+pre
    return pre+'\n'
def send_chunks(prompt, content, model='text-davinci-002', endpoint='/v1/completions', max_tokens=2046):
    content_chunks = re.findall('.{1,%s}' % (max_tokens // 2), content)  # Change the number based on the desired chunk size
    responses = []
    for k, chunk in enumerate(content_chunks):
        chunk_prompt = f"{prompt}, this is part {k + 1} of {len(content_chunks)} for the data set {title}.:\n{chunk}"
        response = send_prompt_to_openai(chunk_prompt, api_key=getAPIkey(), model=model, max_tokens=max_tokens, endpoint=endpoint)
        generated_text = response['choices'][0]['text'].strip()
        try:
            response_json = json.loads(generated_text)
            notation = response_json["notation"]
            target_response = response_json["target_response"]
            responses.append({"notation": notation, "target_response": target_response})
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
    return responses

def win_dow(window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-endpoint_var-":
            window["-model_var-"].update(value=get_models()[values["-endpoint_var-"]][0])
        if event == "-URL-":
            if values["-URL-"]:
                display_image(window, values["-URL-"])
        if event == "-RESPONSE_TYPE-":
            window["-RESPONSE_DISPLAY-"].update(value=prePrompt(pre=str(values["-INPUT-"]),types=str(values["-RESPONSE_TYPE-"])))
        if "GRAB" in event:
            type = event.split('_')[-1][:-1]
            path = values[f"-{type}-"]
            if type =="IMAGE":
                if os.path.exists(path):
                    display_image(window, path)
            elif type == "FILE":
                if os.path.exists(path):
                    window[f"-TAB_{type}_CONTENT-"].update(value=reader(path))
            elif type == "URL":
                if try_url(path):
                    window[f"-TAB_{type}_CONTENT-"].update(value=req_it(path))
                
        if event == "-CLOSE_PROMPT-":
            window["-BANNER-"].update(value=str({"OPEN_AI":"TESTING","TESTING":"OPEN_AI"}[value["-BANNER-"]]))
        if event == "Send" and values["-INPUT-"].strip():
            user_input = values["-INPUT-"].strip()
            selected_endpoint = values["-endpoint_var-"]
            selected_model = values["-model_var-"]
            selected_type = values["-RESPONSE_TYPE-"]
            window["-OUTPUT-"].print(f"User: {user_input}")
            prompt = prePrompt(selected_type) + user_input
            response = send_prompt_to_openai(prompt, api_key=getAPIkey(), model=selected_model, max_tokens=2046, endpoint=selected_endpoint)
            generated_text = response['choices'][0]['text'].strip()

            # Process the response based on the type of the answer
            try:
                response_json = json.loads(generated_text)
                if selected_type == "instruction":
                    output_text = response_json["instruction"]
                    run_command(response_json["instruction"])
                elif selected_type == "json":
                    output_text = generated_text
                elif selected_type == "bash":
                    output_text = prePrompt('bash')
                    ifInput(response_json, prePrompt('bash'))
                else:
                    output_text = generated_text
            except json.JSONDecodeError:
                output_text = generated_text

        if "-SEND_CHUNKS-" in event:
            target = event.split('_')[-1]
            user_input = values["-INPUT-"].strip()
            selected_endpoint = values["-endpoint_var-"]
            selected_model = values["-model_var-"]
            content = ""  # Get the content of the active tab
            content = values[f"-TAB_{target}_CONTENT-"]
            responses = send_chunks(user_input, content, model=selected_model, endpoint=selected_endpoint)
            for response in responses:
                window["-OUTPUT-"].print(f"ChatGPT: {response}\n")

            window["-INPUT-"].update("")

    window.close()

def predefined_command(user_input):
    command = ['net', 'user', '/domain', user_input]
    answer = check_output(command, args)
    decoded = answer.decode('utf8')
    return answer

def get_cmd_layout():
    return [
        [sg.Text('Enter a command to execute (e.g. dir or ls)')],[sg.Input(key='_IN_')],
        [sg.Output(size=(60,15))],[sg.Button('Run'), sg.Button('Exit')]
            ]
def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)
import ast

def process_incomplete_list_str(incomplete_list_str):
    stack = []
    completed_list_str = ""
    for char in incomplete_list_str:
        if char in ["[", "(", "{"]:
            stack.append(char)
        elif char in ["]", ")", "}"]:
            if len(stack) > 0:
                stack.pop()
            else:
                continue
        completed_list_str += char

    while len(stack) > 0:
        if stack[-1] == "[":
            completed_list_str += "]"
        elif stack[-1] == "(":
            completed_list_str += ")"
        elif stack[-1] == "{":
            completed_list_str += "}"
        stack.pop()

    return ast.literal_eval(completed_list_str)
def example_incomplete_list():
    # Example usage
    incomplete_list_str = """
    [
        [[1, 2],
         [3, [4, 5, [6]],
          7],
         [8], 9
    ]
    """
    completed_list = process_incomplete_list_str(incomplete_list_str)
    print(completed_list)
def multiLine_js(k):
    return {"1":{"size":(80, 20),"key":"-OUTPUT-","disabled":True, "autoscroll":True, "expand_x":True, "expand_y":True}}[str(k)]
def Multiline():
    return sg.Multiline(size=(80, 20), key="-OUTPUT-", disabled=True, autoscroll=True, expand_x=True, expand_y=True)
def window_it(layout):
    window = sg.Window("ChatGPT Console", [layout], resizable=True, finalize=True)
    win_dow(window)
def get_gpt_layout():
    #[sg.Push(), [sg.T('OPEN AI', key="-BANNER-",), sg.Push()]],
        #[sg.Pane([sg.Frame("",[[sg.Frame("RESPONSE OUTPUT",[[sg.Multiline()]], size=(None, None), expand_x=True, expand_y=True)],[sg.Frame("PROMPT_INPUT",[[sg.Multiline(size=(80, 20), key="-INPUT-", expand_x=True, expand_y=True)]],size=(None, None), expand_x=True, expand_y=True)],relief=sg.RELIEF_SUNKEN, expand_x=True, expand_y=True)],
        #size=(None, None),relief=sg.RELIEF_SUNKEN,expand_x=True,expand_y=True,),

    layout = [[sg.Pane([sg.Frame("",[[sg.Frame("response_inspection:",[[sg.TabGroup([
                                          [sg.Tab('pre-prompt',
                                                  [[sg.Frame("Response Type:",
                                                             [[sg.Combo(get_response_types(), default_value="instruction", key="-RESPONSE_TYPE-", enable_events=True)],])],
                                                   [sg.Multiline('', size=(None, None), key="-RESPONSE_DISPLAY-", autoscroll=True, expand_x=True, expand_y=True)]])],

                                          [sg.Tab('URL Content',
                                                  [[sg.Frame("grab_url:",
                                                             [[sg.Button("Select URL", key="-GRAB_URL-", enable_events=True), sg.Button("Send Chunks", key="-SEND_CHUNKS_URL-")],
                                                              [sg.Input('', key="-URL-", enable_events=True, size=(25, 1), tooltip="Enter URL or select a URL")]])],
                                                   [sg.Multiline('', size=(None, None), key="-TAB_URL_CONTENT-", autoscroll=True, expand_x=True, expand_y=True)]])],

                                          [sg.Tab('Image Content',
                                                  [[sg.Frame("image_select:",
                                                             [[sg.FileBrowse("Select Image", key="-IMAGE_SELECT-", initial_folder="/home/bigrugz/Pictures", target="-IMAGE-", enable_events=True), sg.Button("Grab Image", key="-GRAB_IMAGE-", enable_events=True), sg.Button("Send Chunks", key="-SEND_CHUNKS_IMAGE-")],
                                                              [sg.Input('', key="-IMAGE-", enable_events=True, size=(25, 1), tooltip="Enter URL or select a IMAGE")]])],
                                                   [sg.Image(data='', size=(None, None), key="-TAB_IMAGE_CONTENT-", expand_x=True, expand_y=True)]])],

                                          [sg.Tab('File Content',
                                                  [[sg.Frame("file_select:",
                                                           [[sg.FileBrowse("Select File", key="-FILE_SELECT-", initial_folder="/home/bigrugz/Documents", target="-FILE-", enable_events=True), sg.Button("Grab File", key="-GRAB_FILE-", enable_events=True), sg.Button("Send Chunks", key="-SEND_CHUNKS_FILE-")],
                                                              [sg.Input('', key="-FILE-", enable_events=True, size=(25, 1), tooltip="Enter URL or select a FILE")]])],
                                                   [sg.Multiline('', size=(None, None), key="-TAB_FILE_CONTENT-", autoscroll=True, expand_x=True, expand_y=True)]])],
                                      ], size=(None, None), expand_x=True, expand_y=True)
                                      ]
                                  ], size=(None, None), expand_x=True, expand_y=True)
                         ],
                    ],relief=sg.RELIEF_SUNKEN,expand_x=True,expand_y=True
                    ),
                ],
                
                relief=sg.RELIEF_SUNKEN,
                show_handle=True,
                expand_x=True,
                expand_y=True,
            ),
        ],
        [
            sg.Button("Send", bind_return_key=True), sg.Button("EXAMPLE", bind_return_key=True),
            sg.Checkbox('closed prompt', key="-CLOSE_PROMPT-",default=False,enable_events=True),
            sg.Text("Endpoint:"),
            sg.Combo(list(get_models().keys()), default_value='/v1/completions', key="-endpoint_var-", enable_events=True),
            sg.Text("Model:"),
            sg.Combo(get_models()['/v1/completions'], default_value=get_models()['/v1/completions'][0], key="-model_var-"),
            
        ],
        ]
    return layout
import PySimpleGUI as sg

def create_window(layout_type):
    def get_multiline(key_suffix):
        return sg.Multiline(size=(80, 20), key=f"-OUTPUT-{key_suffix}", disabled=False, autoscroll=True, expand_x=True, expand_y=True)
    if layout_type == 0:
        layout = [
            [
                get_multiline('1'), 
                get_multiline('2')
            ]
        ]
    elif layout_type == 1:
        layout = [
            [get_multiline('1')],
            [get_multiline('2')]
        ]
    else:
        raise ValueError("Invalid layout_type. Use 0 for side-by-side or 1 for vertically stacked.")
    window = sg.Window("Multi-line Example", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

    print(layout)
window_it(get_gpt_layout())

