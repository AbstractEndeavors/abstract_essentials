import openai
import json
from datetime import datetime
import os
import requests
import threading
import queue
import speech_to_text
import PySimpleGUI as sg
from gtts import gTTS
from gui_temp import *
from playsound import playsound
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
def pen(filename:str, text:str):
    with open(filename, 'w') as f:
        f.write(text)
def get_glob(obj:str='',glob=globals()):
    if obj in glob:
        return glob[obj]
def default_prompt():
    return 'i forgot to make a prompt, whats up though dogg??? any advice?'
def default_model():
    return 'gpt-4'
def default_tokens():
    return 8192
def default_endpoint():
    return 'https://api.openai.com/v1/chat/completions'
def load_api_key():
    openai.api_key = getAPIkey()
def getAPIkey():
    load_dotenv('/home/hmmm/.env')
    return os.getenv('OPENAI_API_KEY')
def save_audio(txt):
  myobj = gTTS(text=txt, lang='en', slow=False)
  myobj.save("welcome.mp3")
  os.system("mpg321 welcome.mp3")
def play_audio():
  playsound("welcome.mp3")
def headers():
    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {getAPIkey()}'}
def count_tokens(text):
    return len(word_tokenize(text))
def check_token_size(prompt_data: dict, max_tokens: int) -> int:
    message_tokens = sum([count_tokens(message["content"]) for message in prompt_data["messages"]])
    max_tokens = max_tokens - message_tokens
    if max_tokens < 1:
        raise Exception("Max tokens reduced to less than 1, please adjust your messages or max tokens.")
    return max_tokens
def title_instruction_prompt(prompt):
    title_instruction = "Please respond in a JSON format with keys 'title' 'response'. 'title' should contain a single, declarative sentence that summarizes query request"
    return f"{title_instruction} {prompt}"
def extract_title_from_response(response: str) -> str:
    # Parse JSON response
    try:
        response_json = json.loads(response)
        # Extract title
        title = response_json['title']
    except:
        title = ''
    return title
def create_prompt(js:dict=None, model:str=default_model(), prompt:str=default_prompt(), max_tokens: int =default_tokens()) -> dict:
    if js is None or not isinstance(js, dict):
        js = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    else:
        js.setdefault("model", model)
        js.setdefault("prompt", prompt)
        js.setdefault("max_tokens", max_tokens)
    prompt_data = {"model": js['model'], "messages": [{"role": "user", "content": f'{js["prompt"]}' }], "max_tokens": js['max_tokens']}
    prompt_data["max_tokens"] = check_token_size(prompt_data, prompt_data['max_tokens'])
    return prompt_data

def make_request(js:dict ={},endpoint:str=default_endpoint(), que=queue.Queue()):
    response = requests.post(endpoint, json=create_prompt(js), headers=headers())
    print(response)
    try:
      response = response.json()['choices'][0]['message']['content']
    except:
      response = response.text
    que.put(response)  # Put the result in the queue
def create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def save_conversation(model: str, title: str, data: dict):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # get the current timestamp
    filename = f'{timestamp}_{title}.json'
    # Create directories if they don't exist
    create_dir(f'raw_conversations/{model}')
    # Write data to the file
    with open(f'raw_conversations/{model}/{filename}', 'w') as f:
        json.dump(data, f, indent=4)
def browse_and_open_json():
    # layout
    layout = [[sg.Text("Select a JSON file to open:")],
              [sg.Input(), sg.FileBrowse(file_types=(("JSON Files", "*.json"),))],
              [sg.Button("Open")]]
    
    # create window
    window = sg.Window("File Browser", layout)
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        elif event == "Open":
            if values[0] == "":
                sg.popup("No file selected!")
            else:
                with open(values[0], "r") as file:
                    data = json.load(file)
                    prompt = ''
                    if 'prompt' in data:
                        prompt = data['prompt']
                    if 'query' in data:
                        prompt = data['query']
                    # You can now use this 'data' dictionary in your function, for example:
                    while_basic_events(
                        get_gui_fun(
                            'Window',
                            {
                                "title":'chat GPT output',
                                "layout":[
                                    [get_gui_fun('T',{'text':'query: '}),
                                     get_gui_fun('Multiline', {"default_text": prompt,"size": (None, None),"scrollable": True,"auto_size_text": True,"expand_x": True,"expand_y": True})],
                                    [get_gui_fun('T',{'text':'response: '}),get_gui_fun('Multiline', {"default_text": data['response'],"size": (None, None),"scrollable": True,"auto_size_text": True,"expand_x": True,"expand_y": True}),
                                     [get_gui_fun('Button',{"button_text":'Play Audio',"key":'-PLAY_AUDIO-'})]]],
                                "resizable": True,
                                "size": (300, 300)
                            }
                        ),
                        events={
                            '-PLAY_AUDIO-':{
                                "name":"save_play_audio",
                                "instance":None,
                                "global":None,
                                "args":{
                                    "text":{
                                        "type":"get",
                                        "name":"get_value",
                                        "instance":None,
                                        "global":None,
                                        "args":{
                                            "st":"-RESPONSE-"
                                        }
                                    },
                                    "file_path":"new_audio.mp3"
                                }
                            }
                        }
                    )
    window.close()

# Call the function
browse_and_open_json()
def infinite_progress(prompt:str=default_prompt(),progress:int=0,step:int=5,thread=None):
    window = get_gui_fun('Window', {
    "title": 'awaiting open ai response...',
    "layout": [
        [get_gui_fun('Multiline', {
            "default_text": prompt,
            "size": (None, None),
            "scrollable": True,
            "auto_size_text": True,
            "expand_x": True,
            "expand_y": True
        })],
        [get_progress_bar()],
        [get_gui_fun('T', {"text": "Status: Awaiting response...", "key": "-STATUS-"})]  # Status field
    ],
    "resizable": True,"size": (300, 300),})
    while_progress(win=window,progress=progress,step=step,thread=thread)
    
    # Once processing is complete, update the status field
    window["-STATUS-"].update("Status: Response received.")

def raw_data(prompt:str=default_prompt(),js:dict={},model:str=default_model(),endpoint:str=default_endpoint(),max_tokens:int=default_tokens(),que=queue.Queue()):
    if 'prompt' not in js:
        if len(str(prompt)) == 0:
          prompt = 'i forgot to make a prompt, whats up though dogg??? any advice?'
        js['prompt'] = prompt
    js['prompt'] = title_instruction_prompt(js['prompt'])
    message_tokens = sum([len(js['prompt']) for message in js['prompt']])
    js['max_tokens'] = max_tokens-10 -(int(message_tokens)- int(check_token_size(create_prompt(js),int(message_tokens))))
    # Start the request in a separate thread
    thread = get_thread(target=make_request, args=(js, endpoint, que), daemon=True)
    start_thread(thread)
    # Start the progress bar
    infinite_progress(prompt=js['prompt'],thread=thread)
    thread.join()  # Wait for the request to finish if it hasn't already
    response = que.get()
    title = extract_title_from_response(response)
    data = {'prompt': js['prompt'], 'response': response}
    # Save the conversation
    save_conversation(model, title, data)
    return data
def voice_prompts():
    while True:
      save_audio(raw_data(prompt=speech_to_text.main()))
      play_audio()
def parse_bash_script(response):
    bash_script_name = response["data"]["bash_script"]
    contents = response["data"]["contents"]
    
    # Join the contents with a newline to create the script
    script = '\n'.join(contents)

    # Save the script to a file
    with open(bash_script_name, "w") as file:
        file.write(script)
def text_output():
    while True:
        js = raw_data(prompt=speech_to_text.main())
        pen(text=json.dumps(js),filename='output.json')
        while_basic_events(get_gui_fun('Window',{"title":'chat GPT output', "layout":[[get_gui_fun('T',{'text':'query: '}),
                                                                        get_gui_fun('Multiline', {"default_text": js['prompt'],"size": (None, None),"scrollable": True,"auto_size_text": True,"expand_x": True,"expand_y": True})],
                                                                       [get_gui_fun('T',{'text':'response: '}),get_gui_fun('Multiline', {"default_text": js['response'],"size": (None, None),"scrollable": True,"auto_size_text": True,"expand_x": True,"expand_y": True}),
                                                                        [get_gui_fun('Button',{"button_text":'Play Audio',"key":'-PLAY_AUDIO-'})]]],"resizable": True,"size": (300, 300)}),events={'-PLAY_AUDIO-':{"name":"save_play_audio","instance":None,"global":None,"args":{"text":{"type":"get","name":"get_value","instance":None,"global":None,"args":{"st":"-RESPONSE-"}},"file_path":"new_audio.mp3"}}})
browse_and_open_json()
text_output()
