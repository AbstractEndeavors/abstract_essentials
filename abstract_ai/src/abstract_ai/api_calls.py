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
window_mgr,bridge,script_name=create_window_manager(script_name="open_ai_api_call",global_var=globals())
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
def create_chunk_communication(chunk:int=1,total_chunks:int=1,notation:str="",instruction:str=default_instructions(),request:str=None,prompt_data_chunk:str="looks like i didnt send the chunk of data, please a notation if this presents a problem"):
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
def get_current_chunk(chunk:int=1,chunk_data:(list or str)=[]):
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
def create_prompt_js(token_dist:dict=calculate_token_distribution(),prompt_js:dict={},chunk:int=1,total_chunks:int=1,instructions:str=default_instructions(),notation:(bool or str)=True,request:str="i forgot to make a prompt, sorry brobot!",chunk_data:(list or str)=[]):
    """
    Creates a formatted prompt JSON for the API request.

    Returns:
        dict: Formatted prompt JSON.
    """
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
def safe_send(prompt_data:str=default_prompt(),request:str="null",instructions:str=None,model:str=default_model(),title:str=None,prompt_js:dict={},max_tokens:int=default_tokens(),completion_percentage:(int or float)=40,endpoint:str=default_endpoint(),content_type:str='application/json',api_key:str=get_openai_key(),additional_responses:bool=False,directory:str=None):
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
    token_dist=calculate_token_distribution(prompt=prompt_data,max_tokens=max_tokens)
    chunk,output,notation=1,[],""
    if instructions==None:
        instructions=default_instructions(notation=notation,additional_responses=additional_responses)
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
