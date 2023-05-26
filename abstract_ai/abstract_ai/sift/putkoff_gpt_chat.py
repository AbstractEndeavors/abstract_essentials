import openai
import json
import os
import subprocess
import requests
import sys
from subprocess import check_output
import PySimpleGUI as sg
from dotenv import load_dotenv

load_dotenv()
def getAPIkey():
    return os.getenv('OPENAI_API_KEY')
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
                        'commands': [{'description': 'create the index.js file','command':'echo -e "import React from \'react\';\nimport { render } from \'react-dom\';\nimport App from \'./App\';\nimport { BrowserRouter as Router, Route } from \'react-router-dom\';\nimport { Home, About } from \'./routes\';\nrender(<Router>\n  <div>\n    <Route exact path=\'/\' component={Home} />\n    <Route exact path=\'/about\' component={About} />\n  </div>\n</Router>, document.getElementById(\'root\'));" > index.jdef run_command(command)'}]}]}
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"Error running command: {error.decode('utf-8')}")
    if output:
        print(output.decode('utf-8'))
def send_prompt_to_openai(prompt, api_key=getAPIkey(), model='text-davinci-002', max_tokens=2046, endpoint='/v1/completions'):
    url = 'https://api.openai.com{}'.format(endpoint)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {}'.format(api_key)}
    data = {"model":model,'prompt': prompt,'max_tokens': max_tokens}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        raise Exception("Request failed with status code: {}".format(response.status_code))

def prePrompt(pre='',types = ''):
    pre = ''
    js = {'json':'please respond in json format','instruction':'The response should have an "instruction" key containing a textual description, and an "inputs" key containing a list of command line inputs, with each input represented as an object with "type" and "input" keys. For example:\n'+str(getInstruction()),'text':"please respond with text only","bash":"please respond in the form of a bash script"}
    if types in js:
        pre = js[types]+pre
    return pre+'\n'
def win_dow(window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-endpoint_var-":
            window["-model_var-"].update(value=get_models()[values["-endpoint_var-"]][0])
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

            window["-OUTPUT-"].print(f"ChatGPT: {output_text}\n")

            # Clear the input
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
def get_gpt_layout():
    layout = [
        [sg.Multiline(size=(80, 20), key="-OUTPUT-", disabled=True, autoscroll=True)],[sg.Multiline(size=(80, 20), key="-INPUT-")],
        
            [sg.Button("Send", bind_return_key=True),sg.Button("EXAMPLE", bind_return_key=True),
            sg.Text("Response Type:"),
            sg.Combo(get_response_types(), default_value="instruction", key="-RESPONSE_TYPE-"),
            sg.Text("Endpoint:"),
            sg.Combo(list(get_models().keys()), default_value='/v1/completions', key="-endpoint_var-",enable_events=True),
            sg.Text("Model:"),
            sg.Combo(get_models()['/v1/completions'], default_value=get_models()['/v1/completions'][0], key="-model_var-"),
        ],
    ]
        
    window = sg.Window("ChatGPT Console", layout, resizable=True, finalize=True)
    win_dow(window)
get_gpt_layout()
