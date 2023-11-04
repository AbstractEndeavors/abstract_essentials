from abstract_gui import sg,AbstractBrowser,text_to_key,make_component,ensure_nested_list,expandable
from abstract_ai import ModelManager
# Get screen size
# Get screen size
screen_width, screen_height = sg.Window.get_screen_size()
height=0.70
width=0.80
max_size=None
window_height = screen_height*height
window_width=screen_width*width
def calculate_size(percentage, screen_measure):
    return int(screen_measure * percentage / 100)
model_manager = ModelManager()
all_models = model_manager.all_model_names
def get_tokens_by_model(model_name):
    return model_manager._get_max_tokens_by_model(model_name)
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

def generate_bool_text(title,args={}):
    if "key" not in args:
        args["key"]=text_to_key(text=title,section='text')
    return make_component("Frame",title, layout=[[make_component("Multiline",args=args)]],**expandable())
def get_tab_layout(title,layout=None):
    if not layout:
        layout = make_component("Multiline",key=text_to_key(title), **expandable())
    return make_component("Tab",title.upper(),ensure_nested_list(layout))
def make_default_checkbox(title):
    return make_component("Checkbox",title,key=text_to_key(text=title,section='bool'),enable_events=True,default=True)
def get_column(layout,args={}):
    return make_component("Column",ensure_nested_list(layout),**args)
def get_tab_group(grouped_tabs,args={}):
    return make_component("TabGroup",ensure_nested_list(grouped_tabs),**args)

def roles_js():
    return {'assistant':'you are an assistant','Elaborative': 'The model provides detailed answers, expanding on the context or background of the information. E.g., "What is the capital of France?" Answer', 'Socratic': 'The model guides the user to the answer through a series of questions, encouraging them to think critically.', 'Concise': 'The model provides the shortest possible answer to a question.', 'Friendly/Conversational': 'The model interacts in a more relaxed, friendly manner, possibly using casual language or even humor.', 'Professional/Formal': 'The model adopts a formal tone, suitable for professional settings.', 'Role-Playing': 'The model assumes a specific character or role based on user instructions. E.g., "You\'re a medieval historian. Tell me about castles."', 'Teaching': 'The model provides step-by-step explanations or breakdowns, as if teaching a concept to someone unfamiliar with it.', "Debative/Devil's Advocate": 'The model takes a contrarian view to encourage debate or show alternative perspectives.', 'Creative/Brainstorming': 'The model generates creative ideas or brainstorming suggestions for a given prompt.', 'Empathetic/Supportive': 'The model offers emotional support or empathy, being careful not to provide medical or psychological advice without proper disclaimers.'}
def roles_keys():
    return list(roles_js().keys())
def content_type_list():
    return ['application/json','text/plain', 'text/html', 'text/css', 'application/javascript',  'application/xml', 'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp', 'audio/mpeg', 'video/mp4', 'video/webm', 'audio/ogg', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/octet-stream', 'application/zip', 'multipart/form-data', 'application/x-www-form-urlencoded', 'font/woff', 'font/woff2', 'font/ttf', 'font/otf', 'application/wasm', 'application/manifest+json', 'application/push-options+json']

##create_prompt_tab
prompt_tab_keys=['request','prompt Data','chunks','query','instructions']
def get_prompt_tabs(layout_specs={},args={}):
    layout = []
    for prompt_tab_key in prompt_tab_keys:
        layout.append(get_tab_layout(prompt_tab_key,layout=layout_specs.get(prompt_tab_key)))
    return get_tab_group(layout,args=args)

### tokens display
completion_token_keys = ['completion tokens available','completion tokens desired','completion tokens used']
prompt_token_keys = ['prompt tokens available','prompt tokens desired','prompt tokens used']
chunk_data_keys=['max chunk size','chunk length','chunk total']
all_token_keys = completion_token_keys+prompt_token_keys+chunk_data_keys+['chunk sectioned data']
response_types = ['instruction', 'json', 'bash', 'text']
model_type_keys=['role','response type']
percentage_keys = ['prompt percentage','completion percentage']
file_options_keys = ['auto chunk title','reuse chunk data','append chunks','scan mode all']
test_options_keys = ['test run','test files','test file input','test browse']
instructions_keys = ["instructions","additional_responses","suggestions","abort","notation","generate_title","additional_instruction","request_chunks","prompt_as_previous","token_adjustment"]
api_keys = ["header",'api key','api env']
def get_settings():
    def get_tokens_layout():
        def get_tokens_display():
            return [
                [get_tokens_section(create_token_section(completion_token_keys,0.5,[8200,8200,0]))],
                [get_tokens_section(create_token_section(prompt_token_keys,0.5,[8200,8200,0]))],
                [get_tokens_section(create_token_section(chunk_data_keys,0.5,[8200,0,0]))]
                ]
        def get_tokens_section(tokens_dict):
            layout = []
            for title,default_value in tokens_dict.items():
                frame_title = title.split(' ')[0]
                layout.append(make_component("Text",f'{title.split(" ")[-1]}:', auto_size_text=True))
                layout.append(make_component("Input",key=text_to_key(text=title), default_text=default_value,size=(10,1), readonly=True,enable_events=True))
            return make_component("Frame",frame_title,layout=[layout])
        def create_token_section(keys,percentage,values):
            section={}
            for i,key in enumerate(keys):
                section[key]=int(values[i]*percentage)
            return section
        return [make_component("Column",get_tokens_display())]
    ##percentage selection
    def get_percentage_component():
        layout = []
        for key in percentage_keys:
            layout.append(make_component("Column",ensure_nested_list(make_component("Frame",f'{key[:4]} %',layout=ensure_nested_list(make_component("Combo",values=get_num_list(), default_value=50, key=text_to_key(text=key), enable_events=True))))))
        return layout
    def make_file_options_checks(keys):
        layout = []
        for key in keys:
            layout.append(make_component("Checkbox",key,default=True,key=text_to_key(key), enable_events=True))
        return layout
    
    def make_test_options_component():
        layout=[]
        for i,component_name in enumerate(["Checkbox","Checkbox","Input","FilesBrowse"]):
            if component_name == 'Checkbox':
                component =make_component(component_name,test_options_keys[i],default=False,key=text_to_key(text=test_options_keys[i]), enable_events=True)
            else:
                component =make_component(component_name,default=False,key=text_to_key(text=test_options_keys[i]), enable_events=True)
            layout.append(component)
        return layout
    def generate_instructions_bool(instruction_key_list):
        layout = [[]]
        for i,instruction in enumerate(instruction_key_list):
            if i%4==float(0) and i != 0:
                layout.append([])
            layout[-1].append(make_default_checkbox(instruction))
        return layout
    def get_api_options_component():
        layout=[]
        for key in api_keys:   
            layout.append([make_component("Frame",key,ensure_nested_list(make_component("Input",key=text_to_key(text=key), enable_events=True)))])
        return layout
    def get_type_options_component():
        layout=[]
        roles = list(roles_js().keys())
        response_types = ['instruction', 'json', 'bash', 'text']
        values_list= [roles,response_types]
        for i,key in enumerate(model_type_keys):     
            layout.append(make_component("Combo",values=values_list[i], default_value=values_list[i][0], key=text_to_key(text=key), enable_events=True))
        return layout
    ### model selection
    def get_model_selection_layout():
        def get_endpoint_selector():
            return make_component("Frame",'Endpoint',[[make_component("Input",key='-ENDPOINT-', readonly=True, enable_events=True,disabled=True)]])
        def get_model_selector():
            return make_component("Frame",'Model',[[make_component("Combo",all_models, default_value=all_models[0], key='-MODEL-', enable_events=True)]])
        def get_token_display():
            return make_component("Frame",'tokens',[[make_component("Input",get_tokens_by_model(all_models[0]),key='-MAX_TOKENS-', readonly=True, enable_events=True,disabled=True,size=(5,1))]])
        return [[get_endpoint_selector()], [get_model_selector(),get_token_display()]]
    def prompt_options_component():
        return make_file_options_checks(['prompt as recieved'])
    num_list=[5]
    while num_list[-1] < 95:
        num_list.append(num_list[-1]+5)

    title_bool=make_component("Checkbox",'Title', key=text_to_key("title bool",section="bool"), auto_size_text=True, enable_events=True)
    collate_responses=make_component("Checkbox",'Collate Responses', key=text_to_key("collate responses",section="bool"), enable_events=True)
    title_input=make_component("input",key=text_to_key("title text"), enable_events=True)
    instruction_checkboxes=ensure_nested_list(generate_instructions_bool(instructions_keys))
    file_options = ensure_nested_list(make_file_options_checks(file_options_keys))
    test_options= ensure_nested_list(make_test_options_component())
    return [
            [make_component("Frame",'Token Percentage',ensure_nested_list(get_percentage_component()))],
            [make_component("Frame",'Api Options',ensure_nested_list(get_api_options_component()))],
            [make_component("Frame",'Type Options',ensure_nested_list(get_type_options_component()))],
            [make_component("Frame",'prompt options',ensure_nested_list(prompt_options_component()))],
            [make_component("Frame",'Tokens',ensure_nested_list(get_tokens_layout()))],
            [make_component("Frame",'Title',ensure_nested_list([title_bool,title_input]))],
            [make_component("Frame","responses",ensure_nested_list(collate_responses))],
            [make_component("Frame","model select",ensure_nested_list(get_model_selection_layout()))],
            [make_component("Frame","enable instruction", ensure_nested_list(instruction_checkboxes))],
            [make_component("Frame","Test Tools", ensure_nested_list(test_options))],
            [make_component("Frame","file options", ensure_nested_list(file_options))]
        ]
json_tree_layout = [
    [sg.Tree(
        data=sg.TreeData(),
        headings=['Value'],
        auto_size_columns=True,
        num_rows=20,
        col0_width=40,
        key='-JSON-TREE-',
        show_expanded=False,
    )]
]
def get_response():
    output_layout = make_component('Multiline',key='-RESPONSE-',expand_x=True, expand_y=True,size=(None, None),)
    return make_component("Frame",'Response',layout=[[output_layout]], **expandable(size=(400, 400)))
def get_feedback():
    layout = [get_response()]
    sub_sub_layout = []
    sub_layout = []
    for i,title in enumerate(["request_chunks",'abort','additional_responses','suggestions', 'notation','other']):
        if title in ["request_chunks",'abort','additional_responses']:
            component = make_component("Input",key=text_to_key(text=title,section='feedback'),size=(None, 1))
            sub_sub_layout.append(make_component('Frame',title, layout=[[component]]))
        else:
            component = make_component("Multiline",key=text_to_key(text=title,section='feedback'),**expandable(size=(None, 5)))
            sub_layout.append([make_component('Frame',title, layout=[[component]],**expandable())])
    sub_layout = [make_component("Column", ensure_nested_list([sub_sub_layout]+sub_layout), **expandable(size=(None, None), scroll_vertical=True))]
    return [layout,sub_layout]
def get_chunked_sections():
    return [
        [make_component("Button",button_text="CREATE CHUNK",key="-CREATE_CHUNK-",auto_size_text=True, enable_events=True),
         make_component("Checkbox",'custom chunk',default=False,key="-CUSTOM_CHUNK-",auto_size_text=True, enable_events=True)],
        [make_component("Push"),make_component("Button",button_text="<-",key=text_to_key("chunk text back"),enable_events=True),
         make_component("input",default_text='0',key=text_to_key("chunk text number"),size=(4,1)),
         make_component("Button",button_text="->",key=text_to_key("chunk text forward"),enable_events=True),make_component("Push")],
        [make_component("Frame",'chunk sectioned data', layout=[[make_component("Multiline",key=text_to_key('chunk sectioned data'),**expandable())]],**expandable())]]
            
def utilities():
    layout = []
    layout.append(make_component("Tab",'SETTINGS', ensure_nested_list(make_component("Column",get_settings(),**expandable(scroll_vertical=True,scroll_horizontal=True))),**expandable(scroll_horizontal=True))),
    layout.append(make_component("Tab",'RESPONSES', abstract_browser_layout(section='responses'),key=text_to_key(text='response tab'),**expandable(size=(50, 100)))),
    layout.append(make_component("Tab",'Files', abstract_browser_layout(section='files'),**expandable(size=(800, 800)),key=text_to_key(text='file tab'))),
    layout.append(make_component("Tab",'urls', get_urls(),**expandable(size=(800, 800)),key=text_to_key(text='url tab'))),
    layout.append(make_component("Tab",'feedback', get_feedback(),**expandable(size=(800, 800)),key=text_to_key(text='feedback tab')))
    return  make_component("TabGroup",ensure_nested_list(layout),**expandable(size=(800, 800)))
####submit options
def get_output_options():
    return [
        [
         make_component("Button",button_text="SUBMIT QUERY",key="-SUBMIT_QUERY-", disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR INPUT",key='-CLEAR_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="COPY RESPONSE",key='-COPY_RESPONSE-', disabled=False,enable_evete=True),
         make_component("Button",button_text="PASTE INPUT",key='-PASTE_INPUT-', disabled=False,enable_evete=True),
         make_component("Button",button_text="CLEAR CHUNKS",key='-CLEAR_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="UNDO CHUNKS",key='-UNDO_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="REDO CHUNKS",key='-REDO_CHUNKS-', disabled=False,enable_evete=True),
         make_component("Button",button_text="GEN README",key='-GENERATE_README-', disabled=False,enable_evete=True)]
    ]
def get_urls():
    return [
        [make_component("Input",key='-URL-', enable_events=True), make_component("Button",'Add URL',key='-ADD_URL-',enable_events=True), make_component("Listbox",values=[], key='-URL_LIST-', size=(70, 6))],
        [make_component("Button",'GET SOUP',key=text_to_key(text='get soup'),enable_events=True),
         make_component("Button",'GET SOURCE',key=text_to_key(text='get source code'),enable_events=True),
         make_component("Button",'CHUNK_DATA',key=text_to_key(text='add url to chunk'),enable_events=True),
         make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section='url'),size=(20,1))]])],
        [make_component("Multiline",key=text_to_key(text='url text'),**expandable())],
    ]
def abstract_browser_layout(section=None):
    extra_buttons = [make_component("Button",'CHUNK_DATA',key=text_to_key(text='add file to chunk',section=section),enable_events=True),
                     make_component("Frame",'chunk title',layout=[[make_component("Input",key=text_to_key(text='chunk title',section=section),size=(20,1))]])]
    return AbstractBrowser().get_scan_browser_layout(section=section,extra_buttons=extra_buttons)+[[make_component("Multiline",key=text_to_key(text='file text',section=section),**expandable())]]
def get_progress_frame():
    return [
        [
            make_component("Frame", 'PROGRESS', layout=[
                [
                    make_component("InputText", 'Not Sending', key='-PROGRESS_TEXT-', background_color="light blue", auto_size_text=True, size=(10, 20)),
                    make_component("ProgressBar", 100, orientation='h', size=(10, 20), key='-PROGRESS-'),
                    make_component("Input", default_text='0', key=text_to_key("query count"), size=(10, 20), disabled=True, enable_events=True)
                ]
            ]),
            make_component("Frame", 'query title', layout=[
                [
                    make_component("Input", default_text="title of prompt", size=(30, 1), key=text_to_key('title input'))
                ]
            ]),
            make_component('Frame', "response nav", [
                [
                    make_component("Button", button_text="<-", key=text_to_key("response text back"), enable_events=True),
                    make_component("input", default_text='0', key=text_to_key("response text number"), size=(4, 1)),
                    make_component("Button", button_text="->", key=text_to_key("response text forward"), enable_events=True)
                ]
            ])
        ]
    ]
