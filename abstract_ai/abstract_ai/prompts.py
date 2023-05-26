def call_functions_hard(instance, function_name,varis):
    if instance is not None:
        return getattr(instance, function_name)(*varis)
    else:
        return globals()[function_name](*varis)
def default_prompt():
    return "i have sent nothing, my bad, hows your day though??"
def create_prompt(js: dict = None, model: str = get_default_models(), prompt: str = default_prompt(), max_tokens: int = get_default_tokens()) -> dict:
    if js is None or not isinstance(js, dict):
        js = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    else:
        js.setdefault("model", model)
        js.setdefault("prompt", prompt)
        js.setdefault("max_tokens", max_tokens)
    prompt_data = {"model": js['model'], "messages": [{"role": "user", "content": f'{js["prompt"]}' }], "max_tokens": js['max_tokens']}
    prompt_data["max_tokens"] = check_token_size(prompt_data, prompt_data['max_tokens'])
    return prompt_data

def create_prompt(js):
  return {"model": js['model'],"messages": [{"role": "user", "content": f'{js["prompt"]}'}],"max_tokens": js['max_tokens']}
def get_json_response():
  return "the following will need to be in json format, your response will be described in the following descriptions:\n"
def assign_keys(st):
  return f"as a value for the '{st}' key: "
def get_key_desc(st,text):
  return f"{assign_keys(st)}{text}\n"
def get_notation():
  return  get_key_desc("notation","place here any notes for you to maintain context of this prompt going into the next")
def get_title():
  return  get_key_desc("title","you must determine a title if one is not porvided explicitly by the user, should be a very breif description of the task that was given.")
def get_instruction():
  return get_key_desc("instruction","should containing a textual description")
def get_inputs():
  return get_key_desc("inputs",f"""key containing a list of command line inputs, with each input represented as an object with "type" and "input" keys. For example:\n'{str(return_instruction())}'\n'""")
def get_text():
  return get_key_desc("text","please respond with text only")
def get_bash():
  return get_key_desc("bash","please respond in the form of a bash script")
def get_response():
  return get_key_desc("response","place your query response here")
def get_context():
    return get_key_desc("context", "provide any relevant context or dependencies for the task")
def get_security():
    return get_key_desc("security", "describe any necessary security measures or precautions for the task")
def get_formatting():
    return get_key_desc("formatting", "provide instructions on how the output data should be formatted")
def get_validation():
    return get_key_desc("validation", "describe the validation process or rules for the input data")
def get_error_handling():
    return get_key_desc("error_handling", "describe how the AI should handle potential errors during this task")
def get_revision():
    return get_key_desc("revision", """provide revisions according to line number, for example: [{'lines':[20,25],'revision':'this text goes in place of lines [20:25]'},{...}]""")
def return_instruction():
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
def create_prompt_keys(values):
    cou = 0
    output_text = ''
    val = "get_json_response,get_notation,get_title,get_instruction,get_inputs,get_text,get_bash,get_context,get_context,get_security,get_formatting,get_validation,get_error_handling,get_revision".split(',')
    for key in val:
     
        if values[key] == True:
            if cou == 0:
                output_text = get_json_response()
                cou +=1
            output_text += call_functions_hard(None, key, [])
    return output_text


