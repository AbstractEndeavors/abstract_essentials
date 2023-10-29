import os
from abstract_gui import AbstractBrowser,text_to_key,make_component,ensure_nested_list,expandable
from . import ModelManager
def try_title(component):
    try:
        while isinstance(component,list):
            component = component[0]
        title = component.Title
    except:
        title=None
    return title
def get_num_list():
    num_list=[5]
    while num_list[-1] < 95:
        num_list.append(num_list[-1]+5)
    return num_list
model_manager = ModelManager()
all_models = model_manager.all_model_names
def get_tokens_by_model(model_name):
    return model_manager._get_max_tokens_by_model(model_name)
def get_response_types():
    return ['instruction', 'json', 'bash', 'text']
def roles_js():
    return {'assistant':'you are an assistant','Elaborative': 'The model provides detailed answers, expanding on the context or background of the information. E.g., "What is the capital of France?" Answer', 'Socratic': 'The model guides the user to the answer through a series of questions, encouraging them to think critically.', 'Concise': 'The model provides the shortest possible answer to a question.', 'Friendly/Conversational': 'The model interacts in a more relaxed, friendly manner, possibly using casual language or even humor.', 'Professional/Formal': 'The model adopts a formal tone, suitable for professional settings.', 'Role-Playing': 'The model assumes a specific character or role based on user instructions. E.g., "You\'re a medieval historian. Tell me about castles."', 'Teaching': 'The model provides step-by-step explanations or breakdowns, as if teaching a concept to someone unfamiliar with it.', "Debative/Devil's Advocate": 'The model takes a contrarian view to encourage debate or show alternative perspectives.', 'Creative/Brainstorming': 'The model generates creative ideas or brainstorming suggestions for a given prompt.', 'Empathetic/Supportive': 'The model offers emotional support or empathy, being careful not to provide medical or psychological advice without proper disclaimers.'}
def roles_keys():
    return list(roles_js().keys())
def content_type_list():
    return ['application/json','text/plain', 'text/html', 'text/css', 'application/javascript',  'application/xml', 'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp', 'audio/mpeg', 'video/mp4', 'video/webm', 'audio/ogg', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/octet-stream', 'application/zip', 'multipart/form-data', 'application/x-www-form-urlencoded', 'font/woff', 'font/woff2', 'font/ttf', 'font/otf', 'application/wasm', 'application/manifest+json', 'application/push-options+json']
def get_list_Nums(i,k):
    ls=[]
    while i>0:
        ls.append(i)
        i-=k
    return ls
### model selection
def get_endpoint_selector():
    return [
        [make_component("Text",'Endpoint:'), make_component("Input",key='-ENDPOINT-', readonly=True, enable_events=True,disabled=True)]
    ]
def get_model_selector():
    return [
        [make_component("Text",'Model:'), make_component("Combo",all_models, default_value=all_models[0], key='-MODEL-', enable_events=True)]
    ]
def get_token_display():
    return [
        [make_component("Text",'tokens:'), make_component("Input",get_tokens_by_model(all_models[0]),key='-MAX_TOKENS-', readonly=True, enable_events=True,disabled=True)]
    ]
def get_model_selection_layout():
    return [make_component("Column",get_endpoint_selector()), make_component("Column",get_model_selector()),make_component("Column",get_token_display())]
### input output     
def get_input_output():
    return [
        [make_component("Frame",'Response',layout=[[make_component('Multiline',key=text_to_key(text='-RESPONSE-'),**expandable(size=(160, None)))]]),make_component("Column",get_feedback())]
    ]
def get_input_output_layout():
    return [
        make_component("Column",get_input_output())
        ]
### tokens display
def get_tokens_section(tokens_dict):
    layout = []
    
    for title,default_value in tokens_dict.items():
        frame_title = title.split(' ')[0]
        layout.append(make_component("Text",f'{title.split(" ")[-1]}:', auto_size_text=True))
        layout.append(make_component("Input",key=text_to_key(text=title), default_text=default_value,size=(10,1), readonly=True,enable_events=True))
    return [make_component("Frame",frame_title,layout=[layout])]

def get_completion_percentage_dropdown():
    return ensure_nested_list(make_component("Combo",values=get_num_list(), default_value=40, key=text_to_key(text='completion percentage'), enable_events=True))
def get_prompt_percentage_dropdown():
    return ensure_nested_list(make_component("Combo",values=get_num_list(), default_value=60, key=text_to_key(text='prompt percentage'), enable_events=True))
def get_completion_tokens():
    percentage = 4920
    return get_tokens_section({'completion tokens available':percentage,'completion tokens desired':percentage,'completion tokens used':'0'})
def get_prompt_tokens():
    percentage = 3280
    return get_tokens_section({'prompt tokens available':percentage,'prompt tokens desired':percentage,'prompt tokens used':'0'})
def get_chunk_tokens():
        percentage = 3280
        return get_tokens_section({'max chunk size':percentage,'chunk total':'0','chunk length':'0'})
def get_tokens_display():
    return [
        get_completion_tokens(),
        get_prompt_tokens(),
        get_chunk_tokens()
    ]
def get_tokens_layout():
    return [
        make_component("Column",get_tokens_display())
        ]
####tab display
def make_feedback_frame(text_list):
    layout = []
    for i,title in enumerate(text_list):
        if title in ['abort','additional_responses']:
            component = make_component("Input",key=text_to_key(text=title,section='feedback'),size=(10, 1))
        else:
            component = make_component("Multiline",key=text_to_key(text=title,section='feedback'),size=(30, 5))
        layout.append([make_component('Frame',title, layout=[[component]],key=text_to_key(text=title,section='feedback frame'))])
        
    return layout
def get_feedback():
    return [
        make_component("Column",ensure_nested_list(make_feedback_frame(('suggestions', 'notation','abort','additional_responses','other'))))
        ]
"""
    layout = 
    return create_tab_group(component=make_tabs(layout),key=text_to_key(text='feedback',section='tabs'))"""

def create_tab_group(component,key):
    return [
        [
            make_component("TabGroup",ensure_nested_list(component),key=text_to_key(key),**expandable())
        ]
    ]
def create_column_layout(component):
    return [
        make_component("Column",ensure_nested_list(component))
        ]
def make_tabs(components):
    tabs=[]
    for component in components:
        title = try_title(component) or 'tab'
        tabs.append(make_component("Tab",title, ensure_nested_list(component)))
    return ensure_nested_list(tabs)

def prompt_percentage(completion_percentage):
    return 100-completion_percentage
def generate_bool_text(title,args={}):
    args["key"]=text_to_key(text=title,section='text')
    return make_component("Frame",title, layout=[
        
        [make_component("Multiline",args=args)]
    ])
def make_default_checkbox(title):
    return make_component("Checkbox",title,key=text_to_key(text=title,section='bool'),enable_events=True,default=True)
def get_settings():
    num_list=[5]
    while num_list[-1] < 95:
        num_list.append(num_list[-1]+5)
    completion_percentage=ensure_nested_list(make_component("Combo",values=num_list, default_value=60, key=text_to_key(text='completion percentage'), enable_events=True))
    prompt_percentage=ensure_nested_list(make_component("Combo",values=num_list, default_value=40, key=text_to_key(text='prompt percentage'), enable_events=True))
    theme_combo=ensure_nested_list([make_component("Combo",values=make_component("theme_list"), default_value=make_component("theme_list")[0], key=text_to_key(text='theme list'), enable_events=True),make_component("Button",button_text="change theme",key=text_to_key("theme change"),enable_events=True)])
    env_input=ensure_nested_list(make_component("Input",key=text_to_key(text='api env'), enable_events=True))
    role_combo=ensure_nested_list(make_component("Combo",values=roles_keys(), default_value=roles_keys()[0], key=text_to_key(text='role'), enable_events=True))
    generate_title_bool=make_component("Checkbox",'generate title', key=text_to_key("generate title bool"),default=True,auto_size_text=True, enable_events=True)
    title_bool=make_component("Checkbox",'Title', key=text_to_key("title bool"), auto_size_text=True, enable_events=True)
    title_input=make_component("input",key=text_to_key("title text"), enable_events=True)
    header_input=ensure_nested_list(make_component("input",key=text_to_key("header"), enable_events=True))
    api_key=ensure_nested_list(make_component("Input",key=text_to_key(text='api key'), enable_events=True))
    content_type_combo=ensure_nested_list(make_component("Combo",values=content_type_list(), default_value=content_type_list()[0], key=text_to_key(text='content type'), enable_events=True))
    default_checkboxes=([[make_default_checkbox('additional Responses'),make_default_checkbox('Abort')],[make_default_checkbox('additional instruction'),make_default_checkbox('notation'),make_default_checkbox('suggestions')]])
    file_options = ensure_nested_list([[make_component("Checkbox",'auto chunk title',default=True,key=text_to_key('auto chunk title'), enable_events=True),make_component("Checkbox",'reuse chunk data',default=False,key='-REUSE_CHUNK-'),make_component("Checkbox",'append',default=True,key='-APPEND_CHUNK-'),make_component("Checkbox",'all directory',default=True,key='-SCAN_MODE_ALL-')]])
    test_options= ensure_nested_list([[make_component("Checkbox",'Test Run',default=False,key=text_to_key(text='test run'), enable_events=True),make_component("Input",key=text_to_key(text='test file'), enable_events=True),make_component("FileBrowse","Files", enable_events=True, key=text_to_key(text='test browse'))]])
    return [
            [make_component("Frame",'completion percentage',layout=completion_percentage),
             make_component("Frame",'prompt percentage',layout=prompt_percentage),
             make_component("Frame",'change theme',layout=theme_combo),
             make_component("Frame",'content type',layout=content_type_combo),
             make_component("Frame",'api env key',layout=env_input),
             make_component("Frame",'role',layout=role_combo)],
            [make_component("Frame",'api key',layout=api_key),
             make_component("Frame",'header',layout=header_input),
             make_component("Frame",'Title',layout=ensure_nested_list([generate_title_bool,title_bool,title_input])),
            ],
            get_tokens_layout(),
            get_model_selection_layout(),
            [make_component("Frame","enable instruction", layout=default_checkboxes)],
            [make_component("Frame","Test Tools", layout=test_options)],
            [make_component("Frame","file options", layout=file_options)]
            
        ]
def get_instructions():
    
    return [
        
        [generate_bool_text('additional Responses',args={**expandable(size=(40,5))}),generate_bool_text('abort',args={**expandable(size=(40,5))})],[make_component("Frame",'instructions', layout=[[make_component("Multiline",key=text_to_key('instruction'), **expandable())]], **expandable(size=(40,5)))],
        [generate_bool_text('Notation',args={**expandable(size=(40,5))}),generate_bool_text('suggestions',args={**expandable(size=(40,5))}),generate_bool_text('additional Instruction',args={**expandable(size=(80,5))})],
     
            ]
def get_chunked_sections():
    
    return [
        [make_component("Button",button_text="CREATE CHUNK",key="-CREATE_CHUNK-",auto_size_text=True, enable_events=True),make_component("Checkbox",'custom chunk',default=False,key="-CUSTOM_CHUNK-",auto_size_text=True, enable_events=True)],
        [make_component("Push"),make_component("Button",button_text="<-",key=text_to_key("chunk text back"),enable_events=True),make_component("input",default_text='0',key=text_to_key("chunk text number"),size=(4,1)),make_component("Button",button_text="->",key=text_to_key("chunk text forward"),enable_events=True),make_component("Push")],
        [make_component("Frame",'chunk sectioned data', layout=[[make_component("Multiline",key=text_to_key('chunk sectioned data'), **expandable())]], **expandable())]]
            
def get_prompt_query():
    return [
        [make_component("Frame","QUERY", layout=[[make_component("Multiline",key='-PROMPT-', **expandable())]], **expandable())],
     ]
def get_prompt_request():
    return [
        [make_component("Frame","prompt request", layout=[[make_component("Multiline",key='-REQUEST-', **expandable())]], **expandable())]
            ]
def get_prompt_data():
    return [
        [make_component("Frame","prompt Data", layout=[[make_component("Multiline",key='-PROMPT_DATA-', **expandable())]], **expandable())]
            ]
def get_responses():

        
    return [
        [make_component("Input",key='-RESPONSE_DATA_DIRECTORY-', enable_events=True), make_component("FilesBrowse",'Browse',initial_folder=os.getcwd(),key="-BROWSE_FOLDER-")],
        [make_component("Combo",values=[], default_value='', key='-RESPONSE_DIRECTORY_LIST-', enable_events=True), make_component("FilesBrowse",'Browse')],
        [make_component("Multiline",key='-RESPONSE_TEXT-', **expandable())]
        ]
def get_files():
    layout = [
        # Top Row
        [make_component("Frame","Directory Scan", layout=[[
         make_component("InputText",default_text=os.getcwd(), key='-DIR-'),
         make_component("FileBrowse",button_text="Files", enable_events=True, key="files"),
         make_component("FolderBrowse",button_text="Folders", enable_events=True, key="directory")],

        # Middle Row
        [make_component("Listbox",values=[], size=(100, 10), key='FILE', enable_events=True)],
        [make_component("Input",default_text='0', key='chunk text number', enable_events=True)],

        # Bottom Row
        [make_component("Button",button_text="->", key="chunk text forward", enable_events=True),
         make_component("Button",button_text="Scan", key="-SCAN-", enable_events=True),
         make_component("Button",button_text="<-", key="-BROWSE_BACK-", enable_events=True),
         make_component("Button",button_text="File Scan Mode", key="-MODE-", enable_events=True),
         make_component("Button",button_text="->", key="-BROWSE_FORWARD-", enable_events=True),
         make_component("Button",button_text='Select Highlighted', key="-SELECT_HIGHLIGHTED-", enable_events=True)]],**expandable())]
    ]
def abstract_browser_layout(section=None):
    extra_buttons = [make_component("Button",'CHUNK_DATA',key=text_to_key(text='add file to chunk',section=section),enable_events=True),make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section=section),size=(20,1))]])]
    return AbstractBrowser().get_scan_browser_layout(section=section,extra_buttons=extra_buttons)+[[make_component("Multiline",key=text_to_key(text='file text',section=section), **expandable())]]
        
def get_urls():
    return [
        [make_component("Input",key='-URL-', enable_events=True), make_component("Button",'Add URL',key='-ADD_URL-',enable_events=True), make_component("Listbox",values=[], key='-URL_LIST-', size=(70, 6))],
        [make_component("Button",'GET SOUP',key=text_to_key(text='get soup'),enable_events=True),
         make_component("Button",'GET SOURCE',key=text_to_key(text='get source code'),enable_events=True),
         make_component("Button",'CHUNK_DATA',key=text_to_key(text='add url to chunk'),enable_events=True),
         make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section='url'),size=(20,1))]])],
        [make_component("Multiline",key=text_to_key(text='url text'), **expandable())],
    ]
def get_grouped_tabs_left():
    return [
                [make_component("Tab",'PROMPT', get_prompt_request(),**expandable()),
                 make_component("Tab",'PROMPT_DATA',get_prompt_data(),**expandable()),
                 make_component("Tab",'CHUNKS', get_chunked_sections(),**expandable()),
                 make_component("Tab",'PROMPT_QUERY',get_prompt_query(),**expandable()),
                 make_component("Tab",'INSTRUCTIONS', get_instructions(),**expandable()),
                 ]
                ]
def get_grouped_tabs_right():
    return [[
                 make_component("Tab",'SETTINGS', get_settings(),**expandable()),
                 make_component("Tab",'RESPONSES', abstract_browser_layout(section='responses'),key=text_to_key(text='response tab'),**expandable()),
                 make_component("Tab",'Files', abstract_browser_layout(section='files'),**expandable(),key=text_to_key(text='file tab')),
                 make_component("Tab",'urls', get_urls(),**expandable(),key=text_to_key(text='url tab'))
                 ]
                ]
def get_tab_group(grouped_tabs):
    return [
        [
            make_component("TabGroup",grouped_tabs,key='-TABS-',**expandable(size=(800,800)))
        ]
    ]

def get_tabs_layout(tab_group):
    return [
        make_component("Column",tab_group)
        ]
####submit options
def get_output_options():
    return [
        [make_component("Text",'Response Type:', size=(15, 1)),
         make_component("Combo",get_response_types(), default_value=get_response_types()[0], key='-RESPONSETYPE-', readonly=True),
         make_component("Button",button_text="SUBMIT QUERY",key="-SUBMIT_QUERY-", disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR INPUT",key='-CLEAR_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="COPY RESPONSE",key='-COPY_RESPONSE-', disabled=False,enable_evete=True),
         make_component("Button",button_text="PASTE INPUT",key='-PASTE_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR CHUNKS",key='-CLEAR_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="UNDOI CHUNKS",key='-UNDO_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="REDO CHUNKS",key='-REDO_CHUNKS-', disabled=False,enable_evete=True)],
         
    ]
def get_output_options_layout():
    return [
        make_component("Column",get_output_options())
        ]
def get_total_layout():
    tab_group_bottom = get_tabs_layout(get_tab_group(get_grouped_tabs_left()))
    tab_group_bottom.append(make_component("Column",get_tabs_layout(get_tab_group(get_grouped_tabs_right()))))
    return [
        [[make_component("Frame",'PROGRESS',layout=[[
        make_component("Text",'Not Sending',key='-PROGRESS_TEXT-', auto_size_text=True),
        make_component("ProgressBar",100, orientation='h', size=(20, 20), key='-PROGRESS-'),
        make_component("Input",default_text='0',key=text_to_key("query count"),auto_size_text=True, disabled= True,enable_events=True),
        make_component("Frame",'query title',layout=[[make_component("Input",default_text="title of prompt",size=(40,1), key=text_to_key('title input'))]])]]),
              get_output_options()],get_input_output_layout()],
            [tab_group_bottom]
            ]
