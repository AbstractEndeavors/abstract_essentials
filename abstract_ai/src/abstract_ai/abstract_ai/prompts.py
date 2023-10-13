"""
prompts.py
=====================
This module is part of the `abstract_ai` module of the `abstract_essentials` package. It provides functionalities related to prompts, their descriptions, and related operations.

Functions:
----------
- call_functions_hard(instance, function_name, varis) : Calls the specified function name with provided arguments.
- default_prompt() : Returns the default prompt string.
- create_prompt(prompt_js, endpoint, model, prompt, max_tokens) : Creates a prompt dictionary with specified values.
- get_json_response() : Returns a description for the 'response' key in JSON format.
- assign_keys(st) : Returns a description for assigning a value to a specific key.
- get_key_desc(st, text) : Returns a description for a specified key with provided text.
- get_notation() : Returns a description for the 'notation' key.
- get_title() : Returns a description for the 'title' key.
- get_instruction() : Returns a description for the 'instruction' key.
- get_inputs() : Returns a description for the 'inputs' key.
- get_text() : Returns a description for the 'text' key.
- get_bash() : Returns a description for the 'bash' key.
- get_response() : Returns a description for the 'response' key.
- get_context() : Returns a description for the 'context' key.
- get_security() : Returns a description for the 'security' key.
- get_formatting() : Returns a description for the 'formatting' key.
- get_validation() : Returns a description for the 'validation' key.
- get_error_handling() : Returns a description for the 'error_handling' key.
- get_revision() : Returns a description for the 'revision' key.
- return_instruction() : Returns an instruction dictionary for creating a basic react forum.
- create_prompt_keys(values) : Creates output text based on selected keys.

Notes:
------
This module is intricately tied with environment variables and dependent modules. For seamless requests and response handling, ensure proper setup of dependencies and appropriate setting of environment variables.

About abstract_ai
--------------------
part of: abstract_ai
Version: 0.1.7.1
Author: putkoff
Contact: partners@abstractendeavors.com
Content Type: text/markdown
Source and Documentation:
For the source code, documentation, and more details, visit the official GitHub repository.
github: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai

Notes:
------
This module mainly focuses on defining and describing various prompt-related keys for better communication with the API. It helps streamline the process of sending prompts to the OpenAI API by ensuring that they adhere to a consistent format.

"""
from .endpoints import default_model, default_tokens,default_endpoint
def call_functions_hard(instance, function_name, varis):
    """
    Calls the specified function name with the provided arguments on the given instance.

    If the instance is not None, the function is called using `getattr(instance, function_name)(*varis)`.
    If the instance is None, the function is called using `globals()[function_name](*varis)`.

    Args:
        instance (object or None): The instance on which the function is called.
        function_name (str): The name of the function to call.
        varis (tuple): The arguments to pass to the function.

    Returns:
        The result of the function call.
    """
    if instance is not None:
        return getattr(instance, function_name)(*varis)
    else:
        return globals()[function_name](*varis)


def default_prompt():
    """
    Returns the default prompt string.

    Returns:
        str: The default prompt.
    """
    return "I haven't sent anything. How's your day though?"


def create_prompt(prompt_js: dict = None,endpoint:str=default_endpoint(), model: str = default_model(), prompt: str = default_prompt(),
                  max_tokens: int = default_tokens()) -> dict:
    """
    Creates a prompt dictionary with the specified values.

    Args:
        js (dict, optional): The input JSON dictionary. Defaults to None.
        model (str, optional): The model name. Defaults to default_model().
        prompt (str, optional): The prompt string. Defaults to default_prompt().
        max_tokens (int, optional): The maximum number of tokens. Defaults to default_tokens().

    Returns:
        dict: The prompt dictionary.
    """
    if prompt_js is None or not isinstance(prompt_js, dict):
        prompt_js = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    else:
        prompt_js.setdefault("model", model)
        prompt_js.setdefault("prompt", prompt)
        prompt_js.setdefault("max_tokens", max_tokens)
        prompt_js.setdefault("endpoint", endpoint)
    prompt_data = {"model": prompt_js['model'], "messages": [{"role": "user", "content": f'{prompt_js["prompt"]}'}],
                   "max_tokens": prompt_js['max_tokens']}
    return prompt_data


def get_json_response():
    """
    Returns the description for the 'response' key in JSON format.

    Returns:
        str: The description for the 'response' key.
    """
    return "the following will need to be in JSON format, your response will be described in the following descriptions:\n"


def assign_keys(st):
    """
    Returns the description for assigning a value to the specified key.

    Args:
        st (str): The name of the key.

    Returns:
        str: The description for assigning a value to the key.
    """
    return f"as a value for the '{st}' key: "


def get_key_desc(st, text):
    """
    Returns the description for the specified key with the provided text.

    Args:
        st (str): The name of the key.
        text (str): The description text.

    Returns:
        str: The complete description for the key.
    """
    return f"{assign_keys(st)}{text}\n"


def get_notation():
    """
    Returns the description for the 'notation' key.

    Returns:
        str: The description for the 'notation' key.
    """
    return get_key_desc("notation", "place here any notes for you to maintain context of this prompt going into the next")


def get_title():
    """
    Returns the description for the 'title' key.

    Returns:
        str: The description for the 'title' key.
    """
    return get_key_desc("title", "place here any notes for you to maintain context of this prompt going into the next")


def get_instruction():
    """
    Returns the description for the 'instruction' key.

    Returns:
        str: The description for the 'instruction' key.
    """
    return get_key_desc("instruction", "should containing a textual description")


def get_inputs():
    """
    Returns the description for the 'inputs' key.

    Returns:
        str: The description for the 'inputs' key.
    """
    return get_key_desc("inputs", """key containing a list of command line inputs, with each input represented as an object with "type" and "input" keys. For example:\n'{str(return_instruction())}'\n'""")


def get_text():
    """
    Returns the description for the 'text' key.

    Returns:
        str: The description for the 'text' key.
    """
    return get_key_desc("text", "please respond with text only")


def get_bash():
    """
    Returns the description for the 'bash' key.

    Returns:
        str: The description for the 'bash' key.
    """
    return get_key_desc("bash", "please respond in the form of a bash script")


def get_response():
    """
    Returns the description for the 'response' key.

    Returns:
        str: The description for the 'response' key.
    """
    return get_key_desc("response", "place your query response here")


def get_context():
    """
    Returns the description for the 'context' key.

    Returns:
        str: The description for the 'context' key.
    """
    return get_key_desc("context", "provide any relevant context or dependencies for the task")


def get_security():
    """
    Returns the description for the 'security' key.

    Returns:
        str: The description for the 'security' key.
    """
    return get_key_desc("security", "describe any necessary security measures or precautions for the task")


def get_formatting():
    """
    Returns the description for the 'formatting' key.

    Returns:
        str: The description for the 'formatting' key.
    """
    return get_key_desc("formatting", "provide instructions on how the output data should be formatted")


def get_validation():
    """
    Returns the description for the 'validation' key.

    Returns:
        str: The description for the 'validation' key.
    """
    return get_key_desc("validation", "describe the validation process or rules for the input data")


def get_error_handling():
    """
    Returns the description for the 'error_handling' key.

    Returns:
        str: The description for the 'error_handling' key.
    """
    return get_key_desc("error_handling", "describe how the AI should handle potential errors during this task")


def get_revision():
    """
    Returns the description for the 'revision' key.

    Returns:
        str: The description for the 'revision' key.
    """
    return get_key_desc("revision", """provide revisions according to line number, for example: [{'lines':[20,25],'revision':'this text goes in place of lines [20:25]'},{...}]""")


def return_instruction():
    """
    Returns the instruction dictionary for creating a basic react forum.

    Returns:
        dict: The instruction dictionary.
    """
    return {'instruction': ''''Creating a basic react forum requires you to use the create-react-app command line tool. First, install the tool globally to your machine with the command `npm install -g create-react-app`. Then navigate to the folder you want to create the project in, and use the command `create-react-app project-name` to create the project. Next, you'll need to install the required dependencies to build the forum. This can be done with the command `npm install --save react-router react-router-dom` to install the routing library. Finally, you will need to configure the routes and components in the `src/index.js` file.''',
            'inputs': [{'type': 'module', "path": '', 'instruction': 'install react-app global module with npm',
                        "commands": [{"description": "install react-app", "command": 'npm install -g create-react-app'}]},
                       {'type': 'file', 'path': 'src', 'instruction': 'create the app component for the project', 'name': 'App.js',
                        'commands': [{'description': 'make directory', "command": 'mkdir {home_folder}/src/',
                                      'user_input': {'description': 'Please provide the folder path where you want to create the project',
                                                     'item': 'folder', 'name': 'home_folder'}},
                                     {'description': 'create the App.js component',
                                      'command': 'echo -e "import { render, screen } from \'@testing-library/react\';test(\'renders learn react link\', () => {render(<App />);const linkElement = screen.getByText(/learn react/i);expect(linkElement).toBeInTheDocument();});" > App.js'}]},
                       {'type': 'module', 'path': 'src', 'instruction': 'install libraries to build the forum',
                        'commands': [{"description": "install react-router-dom", "command": 'npm install --save react-router react-router-dom'}]},
                       {'type': 'file', 'path': 'src', 'instruction': 'configure the routes and components in the index.js file', 'name': 'index.js',
                        'commands': [{'description': 'create the index.js file', 'command': 'echo -e "import React from \'react\';\nimport { render } from \'react-dom\'"'}]}]}


def create_prompt_keys(values):
    """
    Creates the output text based on the selected keys.

    Args:
        values (dict): The selected key-value pairs.

    Returns:
        str: The output text.
    """
    cou = 0
    output_text = ''
    val = "get_json_response,get_notation,get_title,get_instruction,get_inputs,get_text,get_bash,get_context,get_context,get_security,get_formatting,get_validation,get_error_handling,get_revision".split(',')
    for key in val:

        if values[key] == True:
            if cou == 0:
                output_text = get_json_response()
                cou += 1
            output_text += call_functions_hard(None, key, [])
    return output_text
