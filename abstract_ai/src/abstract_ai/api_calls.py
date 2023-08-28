import os
import json
import requests
import openai
import re
from abstract_utilities.string_clean import eatAll,eatOuter
from abstract_utilities.type_utils import make_bool
from abstract_gui import get_gui_fun,create_window_manager
from abstract_security.envy_it import get_env_value
from .response_handling import save_response
from .tokenization import count_tokens,calculate_token_distribution
from .prompts import default_prompt,create_prompt
from .endpoints import default_model,default_endpoint,default_tokens
def get_openai_key(key:str='OPENAI_API_KEY'):
    """
    Retrieves the OpenAI API key from the environment variables.

    Args:
        key (str): The name of the environment variable containing the API key. 
            Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The OpenAI API key.
    """
    return get_env_value(key=key)

def load_openai_key():
    """
    Loads the OpenAI API key for authentication.
    """
    openai.api_key = get_openai_key()

def headers(content_type:str='application/json',api_key:str=get_openai_key()):
    """
    Generates request headers for API call.
    
    Args:
        content_type (str): Type of the content being sent in the request. Default is 'application/json'.
        api_key (str): The API key for authorization. By default, it retrieves the OpenAI API key.
        
    Returns:
        dict: Dictionary containing the 'Content-Type' and 'Authorization' headers.
    """
    return {'Content-Type': content_type, 'Authorization': f'Bearer {api_key}'}

def post_request(endpoint:str=default_endpoint(), prompt:(str or dict)=create_prompt(),content_type:str='application/json',api_key:str=get_openai_key(),header:dict=None):
    """
    Sends a POST request to the specified endpoint with the provided prompt and headers.
    
    Args:
        endpoint (str): URL endpoint to which the request is sent.
        prompt (str or dict): Prompt or data to be sent in the request.
        content_type (str): Type of the content being sent in the request.
        api_key (str): The API key for authorization.
        header (dict): Optional custom headers. If not provided, default headers will be used.
        
    Returns:
        dict: Response received from the server.
    """
    window_mgr,bridge,script_name=create_window_manager(script_name="open_ai_api_call",global_var=globals())
    if header == None or header is not dict:
        header=headers(content_type,api_key)
    response = requests.post(url=endpoint,json=prompt,headers=header)
    if response.status_code == 200:
        print(f'Request successful with status code {response.status_code}')
    else:
        raise Exception(f'Request failed with status code {response.status_code} \n {response.text}')
    return get_response(response)
def hard_request(prompt: str = default_prompt(), model: str = default_model(), max_tokens: int = default_tokens(),
                 temperature: float = 0.5, top_p: int = 1, frequency_penalty: int = 0, presence_penalty: int = 0):
    """
    Sends a hard request to the OpenAI API using the provided parameters.

    Args:
        max_tokens (int): The maximum number of tokens for the completion.
        prompt (str): The prompt for the API request.

    Returns:
        dict: The response received from the OpenAI API.
    """
    load_openai_key()
    message = {
        "role": "user",
        "content": prompt
    }
    response = openai.ChatCompletion.create(
        model=model,
        messages=[message]
    )
    return response
def quick_request(prompt:str=default_prompt(),max_tokens:int=default_tokens(),model=default_model()):
    """
    Sends a quick request to the OpenAI API using the provided parameters and prints the result.

    Args:
        prompt (str, optional): The prompt for the API request. Defaults to the default_prompt().
        max_tokens (int, optional): The maximum number of tokens for the completion. Defaults to default_tokens().

    Returns:
        None
    """
    return hard_request(max_tokens=max_tokens, prompt=prompt,model=model)
def get_additional_response(bool_value:(bool or str)=False):
    """
    Determines the additional response based on the input value.
    
    Args:
        bool_value (bool or str): Input value based on which the response is determined.
        
    Returns:
        str: The determined response.
    """
    if isinstance(bool_value,str):
        return bool_value
    if bool_value:
        return '"this value is to be returned as a bool value,this option is only offered to the module if the user has allowed a non finite completion token requirement. if your response is constrained by token allowance, return this as True and the same prompt will be looped and the responses collated until this value is False at which point the loop will ceased and promptng will resume once again",'
    return "return False"
def get_notation(bool_value:(bool or str)=False):
    """
    Retrieves the notation based on the input value.
    
    Args:
        bool_value (bool or str): Input value based on which the notation is determined.
        
    Returns:
        str: The determined notation.
    """
    if isinstance(bool_value,str):
        return bool_value
    if bool_value:
        return "insert any notes you would like to recieve upon the next chunk distribution in order to maintain context and proper continuity"
    return "return null"
def get_suggestions(bool_value:(bool or str)=False):
    """
    Retrieves the suggestions based on the input value.
    
    Args:
        bool_value (bool or str): Input value based on which the suggestion is determined.
        
    Returns:
        str: The determined suggestions.
    """
    if isinstance(bool_value,str):
        return bool_value
    if bool_value:
        return "if my prompt request is ambiguious, or i am neglecting something that will benefit your ability to perform the task insertr that here"
    return "return null"
def get_abort():
    """
    Retrieves the abort based on the input value.
    
    Args:
        bool_value (bool or str): Input value based on which the abort is determined.
        
    Returns:
        str: The determined abort.
    """
    if isinstance(bool_value,str):
        return bool_value
    if bool_value:
        return "if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was"
    return "return null"
def get_default(obj:any,default:str):
    """
    Returns the input object if it's a string, the default value if the object is a boolean and True, or None if the object is a boolean and False.
    
    Args:
        obj (any): The object to be analyzed.
        default (str): The default value to return if obj is a boolean and True.
        
    Returns:
        str or None: The input object if it's a string, the default value if obj is a boolean and True, or None otherwise.
    """
    if isinstance(obj,str):
        return obj
    elif obj:
        return default
    return None
def default_instructions(notation:(bool or str)=True,suggestions:(bool or str)=True,additional_responses:(bool or str)=False
,abort:(str or bool)=True):
    """
    Generates a response format template in JSON format.
    
    This function provides a standardized response template for instructions in JSON format. The provided arguments can either be `True` (or a string) to include that section in the response or `False` to exclude it.
    
    Args:
        notation (bool or str, optional): The notation section. Defaults to True.
        suggestions (bool or str, optional): The suggestions section. Defaults to True.
        additional_responses (bool or str, optional): The additional_responses section. Defaults to False.
        abort (str or bool, optional): The abort section. Defaults to True.

    Returns:
        str: A string representation of the desired JSON response format.

    Example:
        Given the arguments `notation=True` and `suggestions="Suggested notes"`, the function returns a JSON-like string with the respective sections filled in or marked for filling.
    """
    
    if get_default(additional_responses,"this value should be true for continued chunks") == None:
        additional_response = False 
    js = {"response": "insert your response",
          "notation": get_default(notation,"insert any notes context,abort reason,etc "),
          "suggestions":get_default(suggestions,"insert any notes context,abort reason,etc "),
          "additional_response":  additional_response,
          "abort": get_default(abort,"True if you cannot fulfill the request"),}
    return 'please respond in json format; the desired response format is as follows in json format, please dont place quotations around the response and use double quotes for the keys and value strings:'+str(js)
def create_chunk_communication(chunk:int=1,total_chunks:int=1,notation:str="",instruction:str=default_instructions(),request:str=None,prompt_data_chunk:str="chunk_null"):
    """
    Creates a formatted communication for the current data chunk.

    Returns:
        str: The formatted chunk communication.
    """
    return f"""this is data chunk {chunk} of {total_chunks} chunks;\n\n the instructions were:\n\n{instruction};\n\n the initial prompt request was:\n\n{request};\n the notation from the previous response was:\n\n{notation};\n\nthis is the current data chunk:\n\n{prompt_data_chunk}"""
def handle_abort(js_prompt):
    """
    Handles an abort scenario and displays a GUI window if necessary.

    Returns:
        bool: True if the request is aborted, False otherwise.
    """
    if make_bool(js_prompt.get("abort")):
        window_layout = [
            get_gui_fun("T", args={"text": js_prompt["suggestions"]}),
            get_gui_fun("Button", args={"button_text": "exit", "enable_events": True, "key": "exit"})
        ]
        window = window_mgr.get_new_window("Query Aborted!!", args={"layout": window_layout})
        window_mgr.while_basic(window)
        return True
def process_response(response):
    """
    Processes the response JSON and returns a dictionary.

    Returns:
        dict: Processed response as a dictionary.
    """
    js_prompt = {}
    try:
        js_prompt = json.loads(response)
    except Exception as e:
        js_prompt = get_response(response)
    return js_prompt
def get_current_chunk(chunk:int=0,chunk_data:(list or str)=[]):
    """
    Returns the current chunk data based on the provided chunk number and chunk data.

    Returns:
        str: Current chunk data.
    """
    if isinstance(chunk_data,str):
        return str
    if isinstance(chunk_data,list):
        return chunk_data[chunk-1]
    return chunk_data

def get_response_from_str(api_response):
    """
    Extracts the response dictionary from a string representation.

    Returns:
        dict: Extracted response dictionary.
    """
    api_response_js = {}
    keys = ["abort","additional_response","suggestions","notation","response"]
    api_response=api_response[len(api_response.split("response")[0])-1:]
    i = 0
    for each in keys:
        key = str('"'+each+'":')
        if key not in api_response:
            key = str('"'+each+'":')
        keys[i]=key
        i+=1
    i=0
    for each in keys:
        key_len = len(api_response.split(each)[0].split(',')[-1])+1+len(each)+len(api_response.split(each)[-1])
        spl = api_response.split(keys[0])
        key = eatAll(keys[i],["'",'"',' ','',':'])
        api_response_js[key]=api_response[-key_len:]
        if i == 0:
            api_response_js[key]=eatOuter(api_response[-key_len:],['',' ','\n','}'])
        api_response=api_response[:-len(api_response_js[key])]
        curr_value = api_response_js[key]
        if len(curr_value) != 0:
            while curr_value[0] !=':' and len(curr_value) >0:
                curr_value=curr_value[1:]
        api_response_js[key]=eatAll(curr_value,['',' ',',','\n',':'])
        i+=1
  
    for key in api_response_js.keys():
        # Remove double quotes around values if they exist
        if api_response_js[key].startswith('"') and api_response_js[key].endswith('"'):
            api_response_js[key] = api_response_js[key][1:-1]
    return api_response_js
def get_response(response):
    """
    Extracts and returns the response dictionary from the API response.

    Returns:
        dict: Extracted response dictionary.
    """
    try:
        resp = response.json()
        return resp
    except:
        return get_response(response.text)
def create_prompt_js(token_dist:dict=None,prompt_js:dict={},chunk:int=1,total_chunks:int=1,instructions:str=default_instructions(),notation:(bool or str)=True,request:str="i forgot to make a prompt, sorry brobot!",chunk_data:(list or str)=[]):
    """
    Creates a formatted prompt JSON for the API request.

    Returns:
        dict: Formatted prompt JSON.
    """
    if token_dist == None:
        token_dist = calculate_token_distribution()
    prompt_js['prompt'] = create_chunk_communication(chunk,total_chunks,notation,instructions,request,get_current_chunk(chunk=chunk,chunk_data=chunk_data))
    prompt_js['max_tokens'] = int(token_dist["completion"]["available"])-count_tokens(instructions)
    return prompt_js
def get_save_output(prompt_js:dict={},endpoint:str=None,api_response:(dict or str)=None,title:any=None,directory:str=None):
    """
    Processes and saves the output after sending a request.
    
    Args:
        prompt_js (dict): The prompt or data sent in the request.
        endpoint (str): URL endpoint to which the request was sent.
        api_response (dict or str): Response received from the server.
        title (any): Optional title for saving the response.
        directory (str): Directory where the response is to be saved.
        
    Returns:
        dict: Processed response.
    """
    response_js = save_response(prompt_js=prompt_js,endpoint=endpoint,response=api_response,title=title,directory=directory)
    if response_js["output"] == False or isinstance(response_js["output"],str):
        if response_js["output"] == False:
            api_response = get_response(api_response)
            response_js["output"] = process_response(api_response.json())
        else:
            response_js["output"]=get_response_from_str(response_js["output"])
    return response_js
def safe_send(prompt_data:str=default_prompt(),request:str="null",instructions:str=None,
              model:str=default_model(),title:str=None,prompt_js:dict={},max_tokens:int=default_tokens(),
              completion_percentage:(int or float)=40,endpoint:str=default_endpoint(),
              content_type:str='application/json',api_key:str=get_openai_key(),
              additional_responses:bool=False,directory:str=None):
    """
    Safely sends a request ensuring the response adheres to the token limitations and other constraints.
    
    Args:
        prompt_data (str): Prompt data for the request.
        request (str): The main request content.
        instructions (str): Instructions for the request.
        model (str): OpenAI model to be used for the request.
        title (str): Title for the request.
        prompt_js (dict): Additional prompt details.
        max_tokens (int): Maximum allowed tokens in the response.
        completion_percentage (int or float): Percentage of completion for the response.
        endpoint (str): URL endpoint to which the request is sent.
        content_type (str): Type of the content being sent in the request.
        api_key (str): The API key for authorization.
        additional_responses (bool): Flag indicating if additional responses are allowed.
        directory (str): Directory where the response is to be saved.
        
    Returns:
        list: List of responses received for the request.
    """
    notation=''
    if instructions==None:
        instructions=default_instructions(notation=notation,additional_responses=additional_responses)
    tokenize_js = {"instructions":instructions,"request":request,"prompt_data":prompt_data,"max_tokens":max_tokens,"completion_percentage":completion_percentage,"chunk_prompt":create_chunk_communication(request=request)}
    token_dist=calculate_token_distribution(tokenize_js=tokenize_js)
    chunk,output,notation=1,[],""
    total_chunks = token_dist["chunks"]["total"]
    chunk_data = token_dist["chunks"]["data"]
    for k in range(total_chunks):
        prompt_js =create_prompt_js(token_dist=token_dist,prompt_js={},instructions=instructions,chunk=chunk,total_chunks=total_chunks,notation=notation,request=request,chunk_data=chunk_data)
        response_loop=True
        while response_loop:
            api_response = post_request(endpoint=endpoint, prompt=create_prompt(prompt_js), header=headers(content_type=content_type,api_key=api_key))
            response_js = get_save_output(prompt_js=prompt_js,endpoint=endpoint,api_response=api_response,title=title,directory=directory)
            output.append(response_js["output"])
            if not make_bool(response_js["output"]["additional_response"]):
                response_loop = False
            notation = response_js["output"]["notation"]
            prompt_js['prompt'] = create_chunk_communication(chunk,token_dist["chunks"]["total"],notation,instructions,request,token_dist["chunks"]["data"][chunk-1])
            prompt_js['max_tokens'] = int(token_dist["completion"]["available"])
            if handle_abort(response_js["output"]):
                break
        if handle_abort(response_js["output"]):
            break
        chunk += 1
    return output
request = """
below is the first module in a packag's readme that will consist of 8 modules total, they all need to be the same format, style and appeal. in the chunked data i will be providing a single module, abstract_modules, which will consist of 3 components, upload_utils.py, module_utils.py, and create_module_folder.py, please create a readme as best you can; the example readme is abstract security
## Abstract Security

**Description:**  
Abstract Security simplifies the management and access of environment variables stored in `.env` files. Its key feature is the ability to search multiple directories for these files, ensuring you always fetch the right environment variables with minimal hassle.

**Dependencies**:
- `os`
- `dotenv`
- Various utilities from `abstract_utilities`

**Functions**:

### 1. `find_and_read_env_file`
- **Purpose**: Search for an environment file and read a specific key from it.
- **Arguments**:
  - `file_name`: Name of the `.env` file to be searched. Defaults to `.env`.
  - `key`: Key to be retrieved from the `.env` file. Defaults to 'MY_PASSWORD'.
  - `start_path`: Directory path to start the search from. Defaults to the current directory.
- **Returns**: The value corresponding to the key if found, otherwise None.

### 2. `search_for_env_key`
- **Purpose**: Search for a specific key in a `.env` file.
- **Arguments**:
  - `path`: The path to the `.env` file.
  - `key`: The key to search for.
- **Returns**: The value of the key if found, otherwise None.

### 3. `check_env_file`
- **Purpose**: Check if the environment file exists in a specified path.
- **Arguments**:
  - `path`: The path to check for the `.env` file.
  - `file_name`: The name of the `.env` file. Defaults to '.env'.
- **Returns**: The path of the `.env` file if it exists, otherwise False.

### 4. `safe_env_load`
- **Purpose**: Safely load the `.env` file if it exists at a specified path.
- **Arguments**:
  - `path`: The path to load the `.env` file from.
- **Returns**: True if the `.env` file is successfully loaded, otherwise False.

### 5. `get_env_value`
- **Purpose**: Retrieves the value of the specified environment variable.
- **Arguments**:
  - `start_path`: The path to the environment file.
  - `file_name`: The name of the environment file. Defaults to '.env'.
  - `key`: The key to search for. Defaults to 'MY_PASSWORD'.
- **Returns**: The value of the environment variable if found, otherwise None.

---


here is a description of pload_utils:

#abstract_modules
# Python Module Upload to PyPI

This utility script allows you to easily upload your Python module to the Python Package Index (PyPI) using Twine. It automates several steps of the packaging and distribution process, making it easier to share your module with the Python community.
Author: putkoff
partOf: abstract_modules
Date: 05/31/2023
Version: 0.0.1.0
author_email: 'partners@abstractendeavors.com'
url: 'https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_utilities'

#abstract_modules
# Python Module Upload to PyPI

This utility script allows you to easily upload your Python module to the Python Package Index (PyPI) using Twine. It automates several steps of the packaging and distribution process, making it easier to share your module with the Python community.
## Usage

Run the script `upload_to_pypi.py` with Python 3:

```bash
python3 upload_to_pypi.py
```

The script will guide you through the following steps:

1. **Selecting Module Directory**: You will be prompted to pick the module directory using a GUI window. This directory should contain the necessary files, including the `setup.py` file.

2. **Updating Version Number**: If the version number in the `setup.py` file matches an existing version in the `dist` directory, you will be asked to enter a new version number.

3. **Building the Module**: The script will build your module using the `setup.py` script. The distribution files (wheels) will be placed in the `dist` directory.

4. **Uploading to PyPI**: The script will prompt you to enter your PyPI username and password securely. It will then upload the module to PyPI using Twine.

5. **Installing the Module**: After successful upload, you will have the option to install the module using pip for testing purposes.

"""

prompt_data='''
upload_utils.py
import os
import math
from abstract_utilities.read_write_utils import read_from_file,write_to_file
from abstract_utilities.cmd_utils import get_sudo_password,get_env_value,get_sudo_password,cmd_run_sudo,cmd_run,pexpect_cmd_with_args
from abstract_utilities.string_clean import eatAll
from abstract_gui import get_browser,create_row_of_buttons,get_gui_fun,create_window_manager,get_yes_no,expandable
from .module_utils import get_installed_versions,scan_folder_for_required_modules
windows_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())
def get_parent_directory(directory: str = os.getcwd()) -> str:
    """
    Opens a file browser to allow the user to pick a module directory and returns the chosen directory.
    If no directory is chosen, it keeps prompting until a selection is made.
    
    :param directory: The initial directory to open the file browser. Defaults to current working directory.
    :return: The path of the selected directory.
    """
    browser_values = None
    while browser_values is None:
        browser_values = get_browser(title="pick a module directory", type="folder", initial_folder=directory)
    return browser_values
def get_output_text(parent_directory: str = os.getcwd()) -> str:
    """
    Generate the path for the output text file based on the provided directory.

    :param parent_directory: Base directory.
    :return: Path to the output text file.
    """
    return os.path.join(parent_directory, 'output.txt')
def install_setup() -> str:
    """
    Return the command to install setup.

    :return: Command string.
    """
    return "sudo python3 setup.py sdist"
def install_twine() -> str:
    """
    Return the command to install twine.

    :return: Command string.
    """
    return "pip3 install build twine --break-system-packages"

def build_module(dist_dir: str) -> str:
    """
    If the 'dist' directory doesn't exist, create it. 
    Return the command to build the module.

    :param dist_dir: Directory to build the module in.
    :return: Command string.
    """
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    return "sudo python3 setup.py bdist_wheel"

def module_upload_cmd() -> str:
    """
    Return the command to upload the module.

    :return: Command string.
    """
    return "python3 -m twine upload dist/*.whl --skip-existing"

def upload_module(output_text: str = get_output_text()) -> str:
    """
    Execute the module upload command and handle the required child runs.

    :param output_text: Path to the output text.
    :return: Response from the command execution.
    """
    return pexpect_cmd_with_args(
        command=module_upload_cmd(),
        child_runs=[
            {"prompt": "Enter your username: ", "pass": None, "key": "PYPI_USERNAME"},
            {"prompt": "Enter your password: ", "pass": None, "key": "PYPI_PASSWORD"}
        ],
        output_text=output_text
    )

def save_new_setup(contents, filepath: str = os.getcwd()):
    """
    Save the new setup contents to a file.

    :param contents: Contents to be written to the file.
    :param filepath: Path to the file.
    """
    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(contents)
def read_setup(filepath) -> dict:
    """
    Read the setup file and extract necessary information.

    :param filepath: Path to the setup file.
    :return: Dictionary with extracted information.
    """
    with open(filepath, 'r', encoding='utf-8') as fh:
        setup_file = fh.read()
    cleaner_ls = ['', ' ', '\n', '\t', '"', "'"]
    version = eatAll(x=setup_file.split('version=')[-1].split(',')[0], ls=cleaner_ls)
    name = eatAll(x=setup_file.split('name=')[-1].split(',')[0], ls=cleaner_ls)
    url = eatAll(x=setup_file.split('url=')[-1].split(',')[0], ls=cleaner_ls)
    install_requires = eatAll(x=setup_file.split('install_requires=')[-1].split(']')[0] + ']', ls=cleaner_ls)
    return {
        "filepath": filepath,
        "file": setup_file,
        "version": version,
        "name": name,
        "url": url,
        "install_requires": install_requires
    }
def get_url(setup_js):
    """
    Determine if the URL in the setup information needs to be updated and prompt the user for changes.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
    """
    if setup_js["url"].split('/')[-1] != setup_js["name"]:
        url_new = setup_js["url"][:-len(setup_js["url"].split('/')[-1])]+setup_js["name"]
        permission = get_yes_no(text=f"would you like to change the url requires from {setup_js['url']} to {url_new}?'")
        windows_mgr.while_quick(windows_mgr.get_new_window(title='version number', args={"layout": [
                [[get_gui_fun("T", {"text": "would you like to change the url requires from {setup_js['url']} to {url_new}?"})],
                [get_gui_fun('Input', {"default_text": url_new, "key": "output"})],
                create_row_of_buttons("OK")]]},exit_events=["OK","Override"]))["output"]
        if permission == 'Yes':
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(install_requires,install_requires_new))
def edit_installs(event):
    """
    Handle the event of editing module installations based on user action.
    
    Args:
        event (str): Event trigger for editing installations.
    """
    if event == "Default":
        windows_mgr.update_values(window=windows_mgr.get_last_window_method(),key="-EDIT_INSTALLS-",value=windows_mgr.get_values()["-DEFAULT_INSTALLS-"])
def get_install_requires(setup_js, project_dir,project_name):
    """
    Get the list of required module installations for the given project directory.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
        project_dir (str): Path to the project directory.
    """
    install_requires_new = get_installed_versions(scan_folder_for_required_modules(folder_path=project_dir,exclude=["setuptools",project_name]))
    if setup_js['install_requires'] != install_requires_new:
        new_text = f"would you like to change the install requires from {setup_js['install_requires']} to :"
        default_length = len(install_requires_new)/len(new_text)
        line = "Multiline"
        if math.ceil(default_length) == 1:
            line = "Input"
        layout =[
            [[get_gui_fun("T",args={"text":new_text})],
             [get_gui_fun(line,args={"default_text":install_requires_new,"key":"-DEFAULT_INSTALLS-","size":(len(new_text),math.ceil(default_length)),"disabled":True}),get_gui_fun("T",args={"text":"?"})],
             get_gui_fun("Multiline",args={"default_text":install_requires_new,"size":(len(new_text),10),"key":"-EDIT_INSTALLS-",**expandable()}),
             ],
            [create_row_of_buttons("Yes","No","Choose Edited","Default")]
            ]
        installs = windows_mgr.while_basic(windows_mgr.get_new_window(title='Install Requirements', args={"layout": layout},event_function="edit_installs",exit_events=["Yes","No","Choose Edited"]))
        event = windows_mgr.get_event(window=windows_mgr.get_last_window_method())
        update = installs["-DEFAULT_INSTALLS-"]
        if event == "Choose Edited":
            update = installs["-EDIT_INSTALLS-"]
        if event not in ["No","exit","Exit","EXIT"]:
            save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(str(setup_js['install_requires']),str(update)))
def organize_versions_from_high_to_low(version_list) -> list:
    """
    Organize the list of version numbers from highest to lowest.
    :param version_list: A list of version numbers to organize.
    :return: A new list of version numbers sorted from highest to lowest.
    """
    sorted_versions = sorted(version_list, key=lambda x: list(map(int, x.split('.'))), reverse=True)
    return sorted_versions

def get_distributions_from_packages(setup_js, version_numbers: list = []) ->list:
    """
    Retrieve distribution versions from package directory and populate the provided version_numbers list.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
        version_numbers (list): List of version numbers to populate.
        
    Returns:
        list: Updated version_numbers list.
    """
    dist_dir = os.path.join(setup_js['filepath'][:-len(os.path.basename(setup_js['filepath']))], 'dist')
    if os.path.isdir(dist_dir):
        dist_list = os.listdir(dist_dir)
        for dist in dist_list:
            rest = dist[len(setup_js['name'] + '-'):]
            version = ''
            while len(rest) > 0 and rest[0] in '0123456789.':
                version += rest[0]
                rest = rest[1:]
            version = version.rstrip('.')
            if version not in version_numbers:
                version_numbers.append(version)
    return version_numbers
def get_version_input(highest) ->str:
    """
    Get user input for a new version number.
    
    Args:
        highest (dict): Dictionary containing version information.
        
    Returns:
        str: New version number provided by the user.
    """
    text = ''
    if highest["exists"] == True:
        text += f"Version number {highest['version']} already exists."
    if highest["exists"] == True:
        text += f"Version number {highest['version']} does not exist."
    if highest["bool"] == False:
        text += f"\nYour version number {highest['version']} is lower than the highest version number {highest['highest']}."
    if highest["bool"] == True:
        text += f"\nYour version number {highest['version']} is the highest version number found."
    text += '\n\nplease enter a new version number:'
    layout = [
        [get_gui_fun("T", {"text": text})],
        [get_gui_fun('Input', {"default_text": highest['highest'], "key": "version_number"})],
        create_row_of_buttons("OK")
    ]
    new_version = windows_mgr.while_basic(windows_mgr.get_new_window(title='Version number', args={"layout": layout},exit_events=["OK", "Override"]))["version_number"]
    return new_version
def get_highest(distributions, version) -> dict:
    """
    Determine the highest version in a list of distributions relative to a given version.
    
    Args:
        distributions (list): List of distribution versions.
        version (str): Version to compare against.
        
    Returns:
        dict: Dictionary containing comparison results.
    """
    highest = {"bool":False,"version":version,"highest":version,"exists":False}
    if highest['version'] in distributions:
        highest["bool"] = False
        highest["highest"] = distributions[0]
        highest["exists"] = True
    if highest['version'] not in distributions:
        highest["exists"] = False
        curr_high = organize_versions_from_high_to_low([distributions[0],version])
        if curr_high[0] == version:
            highest["bool"]=True
            highest["highest"] = version
        if curr_high[0] != version:
            highest["bool"]=False
            highest["highest"] = curr_high[0]
    return highest
def get_all_versions(distributions, installed) -> list:
    """
    Get all versions by combining distributions and installed versions.
    
    Args:
        distributions (list): List of distribution versions.
        installed (list): List of installed versions.
        
    Returns:
        list: List of combined versions, organized from high to low.
    """
    if len(installed) != 0:
        if '=' in installed[0]:
            version_number = installed[0].split('=')[-1]
    if version_number not in distributions:
        distributions.append(version_number)
    return organize_versions_from_high_to_low(distributions)
def finalize_version(setup_js):
    """
    Finalize the version for setup by interacting with the user.
    
    Args:
        setup_js (dict): Dictionary containing setup information.
    """
    version = setup_js['version']
    distributions = get_all_versions(get_distributions_from_packages(setup_js),get_installed_versions([setup_js['name']]))
    while True:
        highest = get_highest(distributions,version)
        if highest["bool"] == False:
            new_version=get_version_input(highest)
            if highest['highest'] == organize_versions_from_high_to_low([highest['highest'],new_version])[0]:
                override_prompt = f"this is still not the highest version number;\nWould you like to override the version number with {new_version}?"
                override = get_yes_no(text=override_prompt)
                if override == "Yes":
                    break
            else:
                version = new_version
        if highest["bool"] == True and highest["exists"] == False:
            break
    save_new_setup(filepath=setup_js['filepath'],contents=read_setup(setup_js['filepath'])["file"].replace(str(setup_js['version']),str(version)))
def install_module(event):
    """
    Install a module based on event trigger.
    
    Args:
        event (str): Event trigger for installation.
    """
    if event == "install_module":
        cmd_run(f'pip install {read_setup(globals()["setup_file_path"])["name"]}=={read_setup(globals()["setup_file_path"])["version"]} --break-system-packages')
        cmd_run(f'pip install {read_setup(globals()["setup_file_path"])["name"]}=={read_setup(globals()["setup_file_path"])["version"]} --break-system-packages')
def install_mods_layout():
    """
    Display installation module layout.
    """
    win=windows_mgr.get_new_window(title="install module",layout=[create_row_of_buttons('install_module','EXIT')],event_function='install_module')
    events = windows_mgr.while_basic(window=win)
def get_list_of_projects(parent_directory) -> str:
    """
    Get a list of projects in the given directory.
    
    Args:
        parent_directory (str): Parent directory to search for projects.
        
    Returns:
        str: Selected project from the list.
    """
    win=windows_mgr.get_new_window(title="list_window",args={"layout":[[get_gui_fun('Listbox',{"values":os.listdir(parent_directory),"size":(25,10),'key':'projects',"enable_events":True}),
                                                                        get_gui_fun('Button',{'button_text':'submit','key':'exit'})]]})
    return windows_mgr.while_basic(window=win)['projects'][0]
def run_setup_loop(parent_directory: str = os.getcwd()) -> str:
    """
    Run the setup process in a loop for a given parent directory.
    
    Args:
        parent_directory (str): Parent directory containing projects.
        
    Returns:
        str: Project directory where setup was run.
    """
    output_text = get_output_text(parent_directory)
    cmd_run_sudo(cmd=install_twine(),key="SUDO_PASSWORD",output_text=output_text)
    project_name = get_list_of_projects(parent_directory)
    project_dir = os.path.join(parent_directory,project_name)
    setup_file_path = os.path.join(project_dir,"setup.py")
    src_dir = os.path.join(project_dir,"src")
    dist_dir = os.path.join(project_dir,"dist")
    setup_js = read_setup(setup_file_path)
    finalize_version(setup_js)
    get_install_requires(setup_js,project_dir,project_name)
    get_url(setup_js)
    print(f"Running setup.py for project: {project_dir}")
    globals()["setup_file_path"]=setup_file_path
    os.chdir(project_dir)
    cmd_run_sudo(cmd=install_setup(),key="SUDO_PASSWORD",output_text=output_text)
    cmd_run_sudo(cmd=build_module(dist_dir),key="SUDO_PASSWORD",output_text=output_text)
    upload_module(output_text=output_text)
    print(f"Completed setup.py for project: {project_dir}")
    install_mods_layout()
    return project_dir
def upload_main(directory: str = os.getcwd()):
    """
    Upload the main program for execution.
    
    Args:
        directory (str): Current working directory.
    """
    parent_directory= get_parent_directory(directory)
    run_setup_loop(parent_directory)


module_utils.py
import os
import ast
import re
import importlib
import inspect
from abstract_gui import get_browser
import pkg_resources
def scan_folder_for_required_modules(folder_path=None,exclude:(str or list)=[]):
    """
    Scan the specified folder for Python files and create a list of necessary Python modules.
    :param folder_path: The path of the folder to scan. If None, a folder will be picked using a GUI window.
    :return: A list of required Python modules based on all Python files found in the folder.
    """
    exclude=list(exclude)
    if folder_path is None:
        folder_path = get_browser(
            title="Please choose the destination for your import scripts to be analyzed",
            initial_folder=os.getcwd()
        )
    
    required_modules = set()

    def visit_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tree = ast.parse(file.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            required_modules.add(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        module_parts = node.module.split('.')
                        if node.level > 0:
                            module_parts = ['.'.join(module_parts[:node.level])] + module_parts[node.level:]
                        module_name = '.'.join(module_parts)
                        for name in node.names:
                            required_modules.add(f'{module_name}.{name.name}')
        except SyntaxError:
            # Skip files with syntax errors
            pass

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                visit_file(file_path)
                
    # Update the required_modules to include submodules
    updated_required_modules = set()
    for module in required_modules:
        if module not in exclude:
            parts = module.split('.')
            for i in range(len(parts)):
                updated_required_modules.add('.'.join(parts[:i+1]))
    
    required_list = list(updated_required_modules)
    return required_list
def get_installed_versions(install_requires):
    """
    Get the version numbers of the installed Python modules listed in 'install_requires'.
    :param install_requires: A list of Python module names with optional version constraints.
    :return: A list of module names with their version numbers appended.
    """
    installed_versions = []
    for requirement in install_requires:
        module_name = requirement.split('>=')[0].split('==')[0].strip()
        
        # Validate module_name and skip if not valid
        if not is_valid_package_name(module_name):
            continue

        try:
            version = pkg_resources.get_distribution(module_name).version
        except pkg_resources.DistributionNotFound:
            # Module not found, skip it and continue
            continue

        # Append the version number to the module name in the required format
        if '>=' in requirement:
            installed_versions.append(f'{module_name}>={version}')
        elif '==' in requirement:
            installed_versions.append(f'{module_name}=={version}')
        else:
            installed_versions.append(f'{module_name}>={version}')

    return installed_versions
def is_valid_package_name(package_name):
    """
    Check if a given package name is a valid Python package name.
    
    Args:
        package_name (str): Package name to be validated.
        
    Returns:
        bool: True if the package name is valid, False otherwise.
    """
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', package_name) is not None

def gather_header_docs(folder_path):
    """
    Gather header documentation from Python modules within a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing Python modules.
        
    Returns:
        str: Concatenated header documentation for classes with docstrings.
    """
    header_docs = ""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, "__doc__"):
                    docstring = inspect.getdoc(obj)
                    if docstring:
                        header_docs += f"{name}:\n{docstring}\n\n"

    return header_docs

'''

output = safe_send(prompt_data=prompt_data,request=request,model="gpt-4",title="test_prompt",
                   completion_percentage=50,additional_responses=False,directory=os.getcwd())
print(output)
