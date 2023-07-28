import os
import json
import requests
import openai
from abstract_security.envy_it import get_env_value
from .response_handling import save_response
from .tokenization import count_tokens,calculate_token_distribution
from .prompts import default_prompt,create_prompt
from .endpoints import default_model,default_endpoint,default_tokens
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
def raw_data(prompt:str=default_prompt(),model=default_model(),js:dict={}, endpoint:str=default_endpoint()):
    """
    Sends a raw data request to the specified endpoint with the provided parameters.

    Args:
        prompt (str, optional): The prompt for the API request. Defaults to default_prompt().
        js (dict, optional): The JSON dictionary containing the request data. Defaults to an empty dictionary.
        endpoint (str, optional): The endpoint for the API request. Defaults to get_default_endpoint().

    Returns:
        dict: The response received from the API request.
    """
    if 'prompt' not in js:
        js['prompt'] = prompt
    if 'max_tokens' not in js:
        js['max_tokens'] = default_tokens()
    js['max_tokens'] = int(js['max_tokens'])
    pre_max = js['max_tokens']
    token_dist=calculate_token_distribution(max_tokens=js['max_tokens'],prompt=js['prompt'],completion_percentage=40)
    total = len(token_dist['chunks']["data"])
    responses = []
    for k in range(0,total):
        bef = int(count_tokens(js['prompt']))
        formatted_prompt = f'part {k} of {total}:\n{token_dist["chunks"]["data"][k]}'
        formatted_prompt_length = count_tokens(formatted_prompt)
        js['prompt'] = formatted_prompt
        js['max_tokens'] = int(float(token_dist["completion"]["available"] - (formatted_prompt_length - bef))*.90)
        response = requests.post(endpoint, json=create_prompt(js), headers=headers())
        resp = save_response(js, response)
        responses.append(response.json()['choices'][0]['message']['content'])
    return responses
        
