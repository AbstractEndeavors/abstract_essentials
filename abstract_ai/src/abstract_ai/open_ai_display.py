import glob
from collections import defaultdict
import openai
import json
import os
import subprocess
import requests
import sys
import PySimpleGUI as sg
import pyperclip
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

# Tokenization and Text Manipulation Functions
def get_keys(js):
    return list(js.keys())
def get_globes(x):
    if x in globals():
        return globals()[x]
def get_from_lsJs(js,st,default):
    keys = get_keys(js)
    for k in range(0,len(keys)):
        key = keys[k]
        ls = js[key]
        if st in ls:
            return key
    return default
def get_default_endpoint():
    endpoint = get_globes('endpoint_selection')
    if endpoint == None:
        endpoint = get_keys(endPoints())[0]
    return change_glob('endpoint_selection',endpoint)
def get_default_models():
    return change_glob('model_selection',endPoints()[get_default_endpoint()][0])
def get_default_tokens():
    model = get_globes('model_selection')
    if model == None:
        model = get_default_model()
    return change_glob('max_tokens',int(get_from_lsJs(get_token_onfo(),model,'2049')))
def select_endpoint_and_model():
    endpoints = endPoints()
    def_ends = get_keys(endpoints)
    def_end = def_ends[0]
    def_models = endPoints()[def_end]
    def_model = def_models[0]
    def_tokens = get_from_lsJs(get_token_onfo(),def_model,'2049')
    sg.theme('Default1')
    layout = [
        [sg.Text("Select an endpoint")],
        [sg.Combo(def_ends, key='-ENDPOINT-',default_value=def_end, size=(60, 1),enable_events=True, readonly=True)],
        [sg.Text("Select a model")],
        [sg.Combo(def_models, key='-MODEL-', default_value=def_model,size=(60, 1),enable_events=True, readonly=True)],
        [sg.Text("Max tokens: "), sg.Text(def_tokens, size=(10, 1), key='-TOKENS-')],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]
    window = sg.Window("Endpoint and Model Selection with Tokens", layout)
    while True:
        event, values = window.read()
        if event == "OK":
            window.close()
            return {"endpoint":change_glob('endpoint_selection',values['-ENDPOINT-']),"model":change_glob('model_selection',values['-MODEL-']),"max_tokens":change_glob('max_tokens',int(get_from_lsJs(get_token_onfo(),values['-MODEL-'],'2049')))}
            break
        elif event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            return {"endpoint":get_default_endpoint(),"model":get_default_models(),"max_tokens":int(get_default_tokens())}
            break
        elif event == '-ENDPOINT-':
            endpoint = values['-ENDPOINT-']
            models = endPoints()[endpoint]
            window['-MODEL-'].update(values=models)
            window['-MODEL-'].update(value=models[0])
            window['-TOKENS-'].update(value=get_from_lsJs(get_token_onfo(),models[0],'2049'))
        elif event == '-MODEL-':
            window['-TOKENS-'].update(value=get_from_lsJs(get_token_onfo(),values['-MODEL-'],'2049'))
    window.close()
def get_token_onfo():
    return {"8192":['gpt-4', 'gpt-4-0314'],"32768":['gpt-4-32k', 'gpt-4-32k-0314'],"4097":['gpt-3.5-turbo', 'gpt-3.5-turbo-0301','text-davinci-003', 'text-davinci-002'],"8001":["code-davinci-002","code-davinci-001"],"2048 ":['code-cushman-002','code-cushman-001'],"2049":['davinci', 'curie', 'babbage', 'ada','text-curie-001','text-babbage-001','text-ada-001']}
def endPoints():
    return {'https://api.openai.com/v1/chat/completions':["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"],
            'https://api.openai.com/v1/completions':["text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"],
            'https://api.openai.com/v1/edits':["text-davinci-edit-001", "code-davinci-edit-001"],
            'https://api.openai.com/v1/audio/transcriptions':['whisper-1'],
            'https://api.openai.com/v1/audio/translations':['whisper-1'],
            'https://api.openai.com/v1/fine-tunes':["davinci", "curie", "babbage", "ada"],
            'https://api.openai.com/v1/embeddings':["text-embedding-ada-002", "text-search-ada-doc-001"],
            'https://api.openai.com/v1/moderations':["text-moderation-stable", "text-moderation-latest"]}
def get_models(endpoint):
    return {'https://api.openai.com/v1/chat/completions':["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"],
            'https://api.openai.com/v1/completions':["text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"],
            'https://api.openai.com/v1/edits':["text-davinci-edit-001", "code-davinci-edit-001"],
            'https://api.openai.com/v1/audio/transcriptions':['whisper-1'],
            'https://api.openai.com/v1/audio/translations':['whisper-1'],
            'https://api.openai.com/v1/fine-tunes':["davinci", "curie", "babbage", "ada"],
            'https://api.openai.com/v1/embeddings':["text-embedding-ada-002", "text-search-ada-doc-001"],
            'https://api.openai.com/v1/moderations':["text-moderation-stable", "text-moderation-latest"]}[endpoint]

def truncate_text(text, max_tokens):
    # Truncates a given text to a specified maximum number of tokens while preserving the integrity of sentences or words.
    tokens = word_tokenize(text)
    if len(tokens) <= max_tokens:
        return text
    truncated_tokens = tokens[:max_tokens]
    truncated_text = ' '.join(truncated_tokens)
    return truncated_text

def chunk_text(text, tokens_per_chunk):
    # Splits a given text into chunks based on the specified number of tokens per chunk.
    tokens = word_tokenize(text)
    chunks = []
    for i in range(0, len(tokens), tokens_per_chunk):
        chunk_tokens = tokens[i:i + tokens_per_chunk]
        chunk = ' '.join(chunk_tokens)
        chunks.append(chunk)
    return chunks

# Utility Functions

def if_lasts(string, endings):
    # Checks if the last characters of a string match any of the specified endings in a list and returns the length of the matching ending.
    for ending in endings:
        if string.endswith(ending):
            return len(ending)
    return 0

def if_toks_count(string, max_tokens, endings):
    # Determines if the token count of a string exceeds a specified value and if the last characters match any specified endings. Returns a boolean flag indicating the condition and the adjusted index.
    tokens = word_tokenize(string)
    if len(tokens) > max_tokens:
        for i in range(len(tokens), 0, -1):
            if i <= max_tokens:
                adjusted_string = ' '.join(tokens[:i])
                adjusted_index = if_lasts(adjusted_string, endings)
                return True, i - adjusted_index
    return False, len(tokens)

def fill_toks(string, max_tokens):
    # Fills a list with substrings of a given string based on a specified token count.
    tokens = word_tokenize(string)
    filled_toks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        filled_toks.append(' '.join(chunk_tokens))
    return filled_toks

def find_toks(text, desired_tokens):
    # Finds the positions to split a text into chunks based on a desired token count.
    tokens = word_tokenize(text)
    token_count = len(tokens)
    chunk_size = token_count // desired_tokens
    remainder = token_count % desired_tokens
    split_points = [0]
    start = 0
    for i in range(1, desired_tokens + 1):
        end = start + chunk_size
        if remainder > 0:
            end += 1
            remainder -= 1
        if end < token_count:
            split_points.append(end)
            start = end
    split_points.append(token_count)
    return split_points

# Token Counting Function

def count_tokens(text):
    # Uses the Natural Language Toolkit (NLTK) library to count the number of tokens in a text.
    tokens = word_tokenize(text)
    return len(tokens)

# GUI Functions

def popup_animation(message):
    # Displays an animated popup window using PySimpleGUI.
    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, message, time_between_frames=100)

def time_it(func):
    # Measures the progress of a process using a progress meter.
    with sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress', pad=(20, 10)) as pb:
        for _ in range(100):
            func()
            pb.update(1)

def copy_to_clip(text):
    # Copies text to the clipboard.
    pyperclip.copy(text)

def paste_from_clip():
    # Retrieves text from the clipboard.
    return pyperclip.paste()

def get_response_types():
    # Returns a list of response types.
    response_types = ['Chat', 'Completion', 'Classification', 'Sentiment']
    return response_types

def get_cmd_layout():
    # Defines the layout for a command input window using PySimpleGUI.
    layout = [
        [sg.Text('Enter a command:')],
        [sg.Input(key='-CMD-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]
    return layout

def runCommand(command):
    # Executes a command in the system shell and captures the output.
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.PIPE).decode()
        return output.strip()
    except subprocess.CalledProcessError as e:
        return str(e)

def return_user_input(window):
    # Returns the user input from a GUI window.
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        sys.exit()
    return values

# Prompt and Chunk Manipulation Functions

def update_display(window, content):
    # Updates the content of a GUI window with the provided prompt.
    window['-OUTPUT-'].update(content)

def win_update(window, element, value):
    # Updates the value of an element in a GUI window.
    window[element].update(value)

def win_read(window):
    # Reads the values and events from a GUI window.
    event, values = window.read()
    return event, values

def get_value(window, element):
    # Retrieves the value of a specific element from a GUI window.
    return window[element].get()

def ret_if(condition, input_string, true_string, false_string=''):
    # Returns a string concatenated with a specific input if it matches a condition, otherwise returns another string.
    if condition:
        return true_string + input_string
    else:
        return false_string

def create_pre_prompt(window, prompt):
    # Creates the pre-prompt section for the GUI window based on user input and updates the relevant token count.
    max_tokens = int(get_value(window, '-MAXTOKS-'))
    endings = ['.', '?', '!']
    adjusted_index = if_lasts(prompt, endings)
    adjusted_prompt = prompt[:max_tokens - adjusted_index]
    win_update(window, '-PROMPT-', adjusted_prompt)
    win_update(window, '-PRETOKS-', count_tokens(adjusted_prompt))
    win_update(window, '-PRETOKENS-', ret_if(adjusted_index, adjusted_prompt, ''))

def get_prompt_data(window):
    # Retrieves the prompt data from the GUI window and updates the token count.
    prompt = get_value(window, '-PROMPT-')
    max_tokens = int(get_value(window, '-MAXTOKS-'))
    endings = ['.', '?', '!']
    condition, adjusted_index = if_toks_count(prompt, max_tokens, endings)
    adjusted_prompt = prompt[:adjusted_index]
    win_update(window, '-PROMPT-', adjusted_prompt)
    win_update(window, '-PROMTOKS-', count_tokens(adjusted_prompt))
    win_update(window, '-PROMTOKENS-', ret_if(condition, adjusted_prompt, ''))

def get_prompt_all(window):
    # Retrieves the complete prompt (pre-prompt + data) from the GUI window and updates the token count.
    pre_prompt = get_value(window, '-PREPROMPT-')
    prompt = get_value(window, '-PROMPT-')
    max_tokens = int(get_value(window, '-MAXTOKS-'))
    endings = ['.', '?', '!']
    condition, adjusted_index = if_toks_count(pre_prompt + prompt, max_tokens, endings)
    adjusted_prompt = pre_prompt + prompt[:adjusted_index]
    win_update(window, '-PROMPT-', adjusted_prompt)
    win_update(window, '-PROMTOKS-', count_tokens(adjusted_prompt))
    win_update(window, '-PROMTOKENS-', ret_if(condition, adjusted_prompt, ''))

def get_content(window):
    # Retrieves the content from the selected tabs in the GUI window.
    selected_tabs = get_value(window, '-TABS-')
    content = ''
    if 'Text' in selected_tabs:
        content += get_value(window, '-TEXT-')
    if 'Files' in selected_tabs:
        selected_files = get_value(window, '-FILES-')
        for file in selected_files:
            with open(file, 'r') as f:
                content += f.read()
    if 'URLs' in selected_tabs:
        urls = get_value(window, '-URLS-')
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content += soup.get_text()
    return content

def calculate_max_chunk_size(window):
    # Calculates the maximum chunk size for splitting the content based on a user input, the number of chunks, and the selected model.
    content = get_content(window)
    max_tokens = int(get_value(window, '-MAXTOKS-'))
    num_chunks = int(get_value(window, '-NUMCHUNKS-'))
    model = get_value(window, '-MODEL-')
    if model == 'gpt-3.5-turbo':
        max_tokens -= 10  # Adjusting for the model's maximum token limit
    max_chunk_size = len(content) // (num_chunks * max_tokens)
    win_update(window, '-MAXCHUNKSIZE-', max_chunk_size)

def create_chunks(window):
    # Creates chunks of content based on a maximum chunk size.
    content = get_content(window)
    max_chunk_size = int(get_value(window, '-MAXCHUNKSIZE-'))
    chunks = chunk_text(content, max_chunk_size)
    win_update(window, '-CHUNKS-', '\n'.join(chunks))

def size_chunks(window):
    # Adjusts the chunk size based on the actual content and the desired maximum chunk size.
    content = get_content(window)
    desired_chunk_size = int(get_value(window, '-MAXCHUNKSIZE-'))
    split_points = find_toks(content, desired_chunk_size)
    chunks = []
    for i in range(len(split_points) - 1):
        chunk = content[split_points[i]:split_points[i+1]]
        chunks.append(chunk)
    win_update(window, '-CHUNKS-', '\n'.join(chunks))

def return_chunk_prompt(window, chunk_num, total_chunks, data_set, chunk):
    # Returns a string representing a chunk prompt with the chunk number, total number of chunks, data set, and the chunk itself.
    prompt = f'Chunk {chunk_num} of {total_chunks} | Data set: {data_set}\n\n{chunk}\n\n'
    return prompt

def get_chunk_prompt(window):
    # Combines the user input, chunk prompt, and selected tabs content to create the final prompt for each chunk.
    user_input = get_value(window, '-INPUT-')
    response_type = get_value(window, '-RESPONSETYPE-')
    selected_tabs = get_value(window, '-TABS-')
    chunks = get_value(window, '-CHUNKS-').split('\n')
    prompts = []
    for i, chunk in enumerate(chunks):
        chunk_num = i + 1
        total_chunks = len(chunks)
        data_set = ret_if('Text' in selected_tabs, 'Text', '', ret_if('Files' in selected_tabs, 'Files', '', 'URLs'))
        prompt = return_chunk_prompt(window, chunk_num, total_chunks, data_set, chunk)
        prompts.append(prompt)
    return prompts

def if_over_float_zero(float_num):
    # Checks if a floating-point number is greater than an integer and returns the appropriate integer value.
    return int(float_num) if float_num > int(float_num) else int(float_num) + 1

def update_tokens(window):
    # Updates the token counts and calculations based on the GUI window values.
    content = get_content(window)
    max_tokens = int(get_value(window, '-MAXTOKS-'))
    pre_prompt_tokens = count_tokens(get_value(window, '-PREPROMPT-'))
    prompt_tokens = count_tokens(get_value(window, '-PROMPT-'))
    content_tokens = count_tokens(content)
    max_chunk_size = int(get_value(window, '-MAXCHUNKSIZE-'))
    num_chunks = if_over_float_zero(content_tokens / max_chunk_size)
    win_update(window, '-PRETOKENS-', pre_prompt_tokens)
    win_update(window, '-PROMTOKENS-', prompt_tokens)
    win_update(window, '-CONTENTTOKENS-', content_tokens)
    win_update(window, '-NUMCHUNKS-', num_chunks)

def get_list_Nums(start, step):
    # Returns a list of numbers based on a starting value and a step size.
    return [str(start + i * step) for i in range(10)]

# Miscellaneous Functions

def predefined_command(command):
    # Executes a predefined command using the check_output function from the subprocess module.
    output = subprocess.check_output(command, shell=True).decode()
    return output

# GUI Layout and Interaction

def get_gpt_layout():
    # Constructs the GUI layout using PySimpleGUI. It includes input and output areas, tabs for different content types, buttons for actions, and selection options for response types, endpoints, and models.
    sg.theme('LightGrey1')
    response_types = get_response_types()
    endpoints = list(endPoints().keys())
    models = get_models(endpoints[0])
    endpoints_layout = [[sg.Text('Endpoint:'), sg.Combo(endpoints, default_value=endpoints[0], key='-ENDPOINT-', readonly=True, enable_events=True)]]
    models_layout = [[sg.Text('Model:'), sg.Combo(models, default_value=models[0], key='-MODEL-', readonly=True, enable_events=True)]]
    input_output_layout = [
        [sg.Text('Input', size=(8, 1)), sg.Multiline(key='-INPUT-', size=(80, 4))],
        [sg.Text('Response', size=(8, 1)), sg.Multiline(key='-RESPONSE-', size=(80, 10))]
    ]
    tabs_layout = [
        [sg.TabGroup([
            [sg.Tab('Text', [[sg.Multiline(key='-TEXT-', size=(80, 20))]]),
             sg.Tab('Files', [[sg.Input(key='-FILES-', enable_events=True), sg.FilesBrowse('Browse')]]),
             sg.Tab('URLs', [[sg.Input(key='-URL-'), sg.Button('Add URL',key='-ADD_URL-', enable_events=True), sg.Listbox(values=[], key='-URLSLIST-', size=(70, 6))]])]],
            key='-TABS-')
        ]
    ]
    chunks_layout = [
        [sg.Text('Max Tokens:', size=(10, 1)), sg.Input(key='-MAXTOKS-', default_text='2048', size=(10, 1), enable_events=True),
         sg.Text('Pre-Tokens:', size=(10, 1)), sg.Input(key='-PRETOKS-', default_text='0', size=(10, 1), readonly=True),
         sg.Text('Pre-Prompt:', size=(10, 1)), sg.Input(key='-PREPROMPT-', size=(40, 1), enable_events=True)],
        [sg.Text('Prompt Tokens:', size=(10, 1)), sg.Input(key='-PROMTOKS-', default_text='32', size=(10, 1), readonly=True),
         sg.Text('Prompt:', size=(10, 1)), sg.Input(key='-PROMPT-', size=(40, 1), enable_events=True),
         sg.Text('Prompt Tokens:', size=(10, 1)), sg.Input(key='-PROMTOKENS-', default_text='0', size=(10, 1), readonly=True)],
        [sg.Text('Content Tokens:', size=(10, 1)), sg.Input(key='-CONTENTTOKENS-', default_text='0', size=(10, 1), readonly=True),
         sg.Text('Max Chunk Size:', size=(12, 1)), sg.Input(key='-MAXCHUNKSIZE-', default_text='256', size=(10, 1), readonly=True),
         sg.Text('Num Chunks:', size=(10, 1)), sg.Input(key='-NUMCHUNKS-', default_text='1', size=(10, 1), readonly=True),
         sg.Text('Chunk Lengths:', size=(12, 1)), sg.Combo(get_list_Nums(1, 1), default_value='1', key='-CHUNKLENGTHS-', readonly=True, enable_events=True)],
        [sg.Text('Chunks:', size=(10, 1)), sg.Multiline(key='-CHUNKS-', size=(80, 6))],
        [sg.Button('Create Chunks'), sg.Button('Size Chunks'), sg.Button('Calculate Max Chunk Size')]
    ]
    output_options_layout = [
        [sg.Text('Response Type:', size=(15, 1)), sg.Combo(response_types, default_value=response_types[0], key='-RESPONSETYPE-', readonly=True)],
        [sg.Button('Submit'), sg.Button('Clear Input'), sg.Button('Copy Response'), sg.Button('Paste Input')]
    ]
    layout = [
        [sg.Column(endpoints_layout), sg.Column(models_layout)],
        [sg.Column(input_output_layout)],
        [sg.Column(tabs_layout)],
        [sg.Column(chunks_layout)],
        [sg.Column(output_options_layout)]
    ]
    return layout

def main():
    # Runs the main event loop for the GUI.
    layout = get_gpt_layout()
    window = sg.Window('ChatGPT', layout, return_keyboard_events=True)
    endpoint = get_value(window, '-ENDPOINT-')
    model = get_value(window, '-MODEL-')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    while True:
        event, values = win_read(window)
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Submit':
            content = get_content(window)
            response_type = get_value(window, '-RESPONSETYPE-')
            response = generate_response(content, response_type, endpoint, model)
            win_update(window, '-RESPONSE-', response)
        if event == 'Clear Input':
            win_update(window, '-INPUT-', '')
        if event == 'Copy Response':
            copy_to_clip(get_value(window, '-RESPONSE-'))
        if event == 'Paste Input':
            win_update(window, '-INPUT-', paste_from_clip())
        if event == '-FILES-':
            win_update(window, '-FILES-', values['-FILES-'])
        if event == '-ADD_URL-':
            url = values['-URL-']
            url_list = get_value(window, '-URLSLIST-')
            url_list.append(url)
            win_update(window, '-URLSLIST-', url_list)
            win_update(window, '-URL-', '')
        if event == '-URLSLIST-':
            url_list = values['-URLSLIST-']
            win_update(window, '-URLSLIST-', url_list)
        if event == '-MAXTOKS-':
            update_tokens(window)
        if event == '-PREPROMPT-' or event == '-PROMPT-':
            get_prompt_data(window)
        if event == '-TABS-':
            get_prompt_all(window)
        if event == 'Create Chunks':
            create_chunks(window)
        if event == 'Size Chunks':
            size_chunks(window)
        if event == 'Calculate Max Chunk Size':
            calculate_max_chunk_size(window)
    window.close()

if __name__ == '__main__':
    main()
