import openai
import json
import os
import requests
import sys
from pathlib import Path
from subprocess import check_output
import PySimpleGUI as sg
from datetime import datetime
from dotenv import load_dotenv
from putkoff_functions import *
from imports.endpoints import *
from imports.message_aggregator import *
import re
env_path = Path.home() / '.env'
load_dotenv(dotenv_path=env_path)
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
def count_tokens(text):
    return len(word_tokenize(text))
env_path = Path.home() / '.env'
load_dotenv(dotenv_path=env_path)
def getAPIkey():
    return os.getenv('OPENAI_API_KEY')
def time_stamp():
    now = datetime.now()
    return datetime.timestamp(now)
def get_time_stamp():
    return datetime.now()
def date():
    return datetime.fromtimestamp(time_stamp()).strftime('%d-%m-%y')
def save_response(js:dict,response:dict,title:str=str(get_time_stamp())):
    generated_text = response.text
    try:
        js['response'] = response.json()
    except:
        print()
    try:
        generated_text = json.loads(js['response']['choices'][0]['message']['content'])
        if 'title' in generated_text:
            title = generated_text['title']
    except:
        print()
    path = mkdirs(os.path.join(mkdirs(os.path.join(mkdirs('response_data'),date())),js['model']))
    pen(os.path.join(path,title+'.json'),json.dumps(js))
    return generated_text
def try_other():
    try:
        js['json'] = response.json()
        model = js['model']
        generated_text = json.loads(js['json']['choices'][0]['message']['content'])
        if 'Title' in generated_text:
            title = generated_text['Title']
        if 'response' in generated_text:
            response = model+': '+generated_text['response']
        input(response)
        # Process the response based on the type of the answer
        try:
            response_json = generated_text
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
    except:
        print()
    pen(os.path.join(path,title+'.json'),json.dumps(js),)
    return response
def combine_js(js,js2):
    keys = get_keys(js2)
    for k in range(0,len(keys)):
        js[keys[k]] = js2[keys[k]]
    return js
def choose_module_components(js={"prompt":''}):
    js = create_prompt(combine_js(js,select_endpoint_and_model()))
    return js
def create_prompt(js):
    return {"model": js['model'],"messages": [{"role": "user", "content": f'{js["prompt"]}'}],"max_tokens": js['max_tokens']}
def headers():
    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {getAPIkey()}'}

def getAPIkey():
    return os.getenv('OPENAI_API_KEY')
def time_stamp():
    now = datetime.now()
    return datetime.timestamp(now)
def get_time_stamp():
    return datetime.now()
def date():
    return datetime.fromtimestamp(time_stamp()).strftime('%d-%m-%y')
def check_token_size(prompt_data: dict, max_tokens: int) -> int:
    message_tokens = sum([count_tokens(message["content"]) for message in prompt_data["messages"]])
    max_tokens = max_tokens - message_tokens
    if max_tokens < 1:
        raise Exception("Max tokens reduced to less than 1, please adjust your messages or max tokens.")
    return max_tokens
def title_generation(model:str = get_default_models()):
    timestamp = str(get_time_stamp())
    ls_dir = os.listdir(mkdirs(os.path.join(mkdirs(os.path.join(mkdirs('response_data'),date())),model)))
    return f"the following will need to be in json format as a value for the 'Title' key: \nGenerate a title for the following query and adhere to the following criteria: No more than 40 characters, use underscores instead of spaces, must not be a title already in {ls_dir},default title should be {timestamp};\nprovide a response to the query;\n the value for the'response' key: should contain the response to the query";
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
def send_chunks(prompt:str =default_prompt(), content:str='', model: str = get_default_models(),endpoint: str = get_default_endpoint(),max_tokens:int = get_default_tokens(),title:str='current'):
    content_chunks = re.findall('.{1,%s}' % (max_tokens // 2), content)  # Change the number based on the desired chunk size
    responses = []
    for k, chunk in enumerate(content_chunks):
        chunk_prompt = f"{prompt}, this is part {k + 1} of {len(content_chunks)} for the data set {title}.:\n{chunk}"
        response = requests.post(endpoint, json=create_prompt({}, model=model, prompt=chunk_prompt, max_tokens=max_tokens, endpoint=endpoint), headers=headers())
        generated_text = response['choices'][0]['text'].strip()
        try:
            response_json = json.loads(generated_text)
            notation = response_json["notation"]
            target_response = response_json["target_response"]
            responses.append({"notation": notation, "target_response": target_response})
        except json.JSONDecodeError:
            print("Error parsing response as JSON")
    return responses
def raw_data(prompt:str =default_prompt(),js: dict = {}, endpoint: str = get_default_endpoint()):
    if 'prompt' not in js:
        js['prompt'] = prompt
    message_tokens = sum([len(js['prompt']) for message in js['prompt']])
    js['max_tokens'] = get_default_tokens()-10 -(int(message_tokens)- int(check_token_size(create_prompt(js),int(message_tokens))))
    return save_response(js,requests.post(endpoint, json=create_prompt(js), headers=headers()))
