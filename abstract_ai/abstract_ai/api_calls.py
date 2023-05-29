import os
import json
import requests
import openai
from abstract_security.envy_it import get_openai_key, getAPIkey
from abstract_utilitites.time_utils import time_stamp,get_time_stamp,date
from .tokenize import count_tokens, check_token_size
from .prompt import default_prompt,create_prompt,default_tokens
def headers():
    """
    Returns the headers for the API request.

    Returns:
        dict: The headers containing the 'Content-Type' and 'Authorization' information.
    """
    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {getAPIkey()}'}


def hard_request(max_tokens, prompt):
    """
    Sends a hard request to the OpenAI API using the provided parameters.

    Args:
        max_tokens (int): The maximum number of tokens for the completion.
        prompt (str): The prompt for the API request.

    Returns:
        dict: The response received from the OpenAI API.
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


def quick_request(prompt: str = default_prompt(), max_tokens: int = default_tokens()):
    """
    Sends a quick request to the OpenAI API using the provided parameters and prints the result.

    Args:
        prompt (str, optional): The prompt for the API request. Defaults to the default_prompt().
        max_tokens (int, optional): The maximum number of tokens for the completion. Defaults to default_tokens().

    Returns:
        None
    """
    print(json.dumps(hard_request(max_tokens, prompt).choices[0].text.strip(), indent=4))


def raw_data(prompt: str = default_prompt(), js: dict = {}, endpoint: str = get_default_endpoint()):
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
    message_tokens = sum([len(js['prompt']) for message in js['prompt']])
    js['max_tokens'] = get_default_tokens() - 10 - (int(message_tokens) - int(check_token_size(create_prompt(js), int(message_tokens))))
    return save_response(js, requests.post(endpoint, json=create_prompt(js), headers=headers()))
