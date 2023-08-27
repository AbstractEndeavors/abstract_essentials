import os
import json
import requests
import openai
from abstract_gui import get_gui_fun,while_quick,create_window_manager
from abstract_utilities.string_clean import eatAll
from abstract_security.envy_it import get_env_value
from ..response_handling import save_response
from ..tokenization import count_tokens,calculate_token_distribution
from ..prompts import default_prompt,create_prompt
from ..endpoints import default_model,default_endpoint,default_tokens
window_mgr,bridge,script_name=create_window_manager(script_name="open_ai_api_call",global_var=globals())
def get_openai_key(key:str='OPENAI_API_KEY'):
    """
    Retrieves the OpenAI API key from the environment variables.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable containing the API key. Defaults to 'OPENAI_API_KEY'.

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
    Returns the headers for the API request.

    Returns:
        dict: The headers containing the 'Content-Type' and 'Authorization' information.
    """
    return {'Content-Type': content_type, 'Authorization': f'Bearer {api_key}'}
def post_request(endpoint:str=default_endpoint(), prompt:(str or dict)=create_prompt(),content_type:str='application/json',api_key:str=get_openai_key()):
        response = requests.post(endpoint, headers=headers(content_type,api_key), json=prompt)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Request failed with status code {response.status_code}')

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

def default_instructions():
    return """please respond in json format; the desired response format is as follows:\n\n{"response":"insert your response","notation":"insert any notes you would like to recieve upon the next chunk distribution in order to maintain context and proper continuity","suggestions":"if my propmpt request is ambiguious, or i am neglecting something that will benefit your ability to perform the task insertr that here","abort":"if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was"}"""
def create_chunk_communication(chunk:int=1,total_chunks:int=1,notation:str="",instruction:str=default_instructions(),request:str=None,prompt_data_chunk:str="looks like i didnt send the chunk of data, please a notation if this presents a problem"):
    return f"""this is data chunk {chunk} of {total_chunks} chunks;\n\n the instructions were:\n\n{instruction};\n\n the initial prompt request was:\n\n{request};\n the notation from the previous response was:\n\n{notation};\n\nthis is the current data chunk:\n\n{prompt_data_chunk}"""
def safe_send(prompt_data:str=default_prompt(),request:str="null",instructions:str=default_instructions(),model:str=default_model(),prompt_js:dict={},endpoint:str=default_endpoint(),max_tokens:int=default_tokens(),completion_percentage:(int or float)=40):
    token_dist=calculate_token_distribution(prompt=prompt_data,max_tokens=max_tokens)
    chunk=1
    output=[]
    notation=""
    for k in range(token_dist["chunks"]["total"]):
        prompt_js['prompt'] = create_chunk_communication(chunk,token_dist["chunks"]["total"],notation,instructions,request,token_dist["chunks"]["data"][chunk-1])
        prompt_js['max_tokens'] = int(token_dist["completion"]["available"])
        prompt = create_prompt(prompt_js)
        response = requests.post(default_endpoint(), json=prompt, headers=headers())
        output.append(json.dumps(save_response(js=prompt,response=response)))
        
        try:
            js_prompt = json.loads(output[-1])
            notation = js_prompt.get("notation", "")
            if js_prompt.get("abort") in ["true", "True", True]:
                window_mgr.while_basic(window_mgr.get_new_window("Query Aborted!!",args={"layout":[get_gui_fun("T",args={"text":js_prompt["suggestions"]}),get_gui_fun("Button",args={"button_text":"exit","enable_events":True,"key":"exit"})]}))
                break
        except Exception as e:
            print(f"Error when processing output: {e}")
            output[-1] = {}
            split_string = response.text.split('","')
            for each in split_string:
                key = each.split(':')[0]
                value = each[len(each.split(':')[0]) + 1:]
                output[-1][eatAll(key, ['{', '}', '', ' ', '\n', '\t'])] = value
        print(output)
        chunk += 1
    return output
#request = "i would kindly ask that you write a detailed, professional, and comprehensive readme for the script endpoints.py. endpoints.py is a script that is part of a larger module named abstract_ai in which the entire package includes the following scripts: [api_calls.py,endpoints.py,prompts.py,response_handling.py,tokenization.py], author: putkoff, email: partners@abstractendeavors.com, github: https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai, pypi: https://pypi.org/project/abstract-ai/, license: MIT, version: 0.1.4.0; \n\n the above will be sent with each data chunk;"
#input(safe_send(prompt_data=prompt_data,request=request,max_tokens=int(int(default_tokens())/2),completion_percentage=60))
