import guitemp
from function_registry import FunctionRegistry
registryendpoint = FunctionRegistry()
def change_glob(x,y):
    globals()[x]=y
    return y
def ret_glob():
    return globals()
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
def update_model(endpoint):
    return endPoints()[endpoint]
def select_endpoint_and_model():
    endpoints = endPoints()
    def_ends = get_keys(endpoints)
    def_end = def_ends[0]
    def_models = endPoints()[def_end]
    def_model = def_models[0]
    def_tokens = get_from_lsJs(get_token_onfo(),def_model,'2049')
    sg.theme('Default1')
    layout = [
        [get_gui_fun('Text',{"Select an endpoint"})],
        [get_gui_fun('Combo',{'values':def_ends,'key':'-ENDPOINT-',"default_value":def_end, "size":(60, 1),"enable_events":True, "readonly":True})],
        [get_gui_fun('Text',{"Select a model"})],
        [get_gui_fun('Combo',{'values':def_models,'key':'-MODEL-',"default_value":def_model,"size":(60, 1),"enable_events":True, "readonly":True})],
        [get_gui_fun('Text',{"Max tokens: "}), get_gui_fun('Text',{"default_value":def_tokens,"size":(10, 1),'key':'-TOKENS-'})],
        [get_gui_fun('Button',"OK"), get_gui_fun('Button','Cancel')]
    ]
    #while_basic_events(get_gui_fun('Window',{"title":"Endpoint and Model Selection with Tokens", "layout":layout}),
    #events={'-ENDPOINT-': {"type": "get","name": 'update','args':{"st":'-MODEL-',"obj":{"type": "get",'name':'update_model',"global":globals(),'args':{"type": "get", "name": "get_value", "args": {'-ENDPOINT-'}}}}}})#,"obj":{"type": "get","global":globals(),"name": 'get_models','args':{"type": "get", "name": "get_value", "args": {"st": '-ENDPOINT-'}}}
            #{"type": "get","global":globals(),"name": "save_play_audio","args": {"text": {"type": "get","global":globals(), "name": "get_value", "args": {"st": "-RESPONSE-"}}, "file_path": "new_audio.mp3"}}}
    while True:
        event, values = window.read()
        if event == "OK":
            window.close()
            return {"endpoint":change_glob('endpoint_selection',values['-ENDPOINT-']),"model":change_glob('model_selection',values['-MODEL-']),"max_tokens":change_glob('max_tokens',int(get_from_lsJs(get_token_onfo(),values['-MODEL-'],'2049')))}
            break
        elif event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            return {"endpoint":get_default_endpoint(),"model":get_default_model(),"max_tokens":int(get_default_tokens())}
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
registryendpoint.register(update_model)

