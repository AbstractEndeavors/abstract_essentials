from abstract_ai_gui_shared import *

def get_tab_layout(title,layout=None):
    if not layout:
        layout = make_component("Multiline",key=text_to_key(title), **expandable())
    return make_component("Tab",title.upper(),ensure_nested_list(layout))
def generate_tab(title, layout):
    return make_component("Tab", ensure_nested_list(layout), **expandable())
def get_prompt_tabs(layout_specs={},args={}):
    layout = []
    for prompt_tab_key in prompt_tab_keys:
        layout.append(get_tab_layout(prompt_tab_key,layout=layout_specs.get(prompt_tab_key)))
    return get_tab_group(layout,args=args)
def get_chunked_sections():
    return [
        [make_component("Button",button_text="CREATE CHUNK",key="-CREATE_CHUNK-",auto_size_text=True, enable_events=True),
         make_component("Checkbox",'custom chunk',default=False,key="-CUSTOM_CHUNK-",auto_size_text=True, enable_events=True)],
        [make_component("Push"),make_component("Button",button_text="<-",key=text_to_key("chunk text back"),enable_events=True),
         make_component("input",default_text='0',key=text_to_key("chunk text number"),size=(4,1)),
         make_component("Button",button_text="->",key=text_to_key("chunk text forward"),enable_events=True),make_component("Push")],
        [make_component("Frame",'chunk sectioned data', layout=[[make_component("Multiline",key=text_to_key('chunk sectioned data'),**expandable())]],**expandable())]]
            
def get_instructions():
    layout = []
    sub_layout = []
    for instruction_key in instructions_keys:
        if instruction_key == 'instructions':
            layout.append(generate_bool_text(instruction_key, args={**expandable(size=(None, 10))}))
        else:
            component = generate_bool_text(instruction_key, args={**expandable(size=(None, 5))})
            sub_layout.append([component])
    sub_layout = [make_component("Column", ensure_nested_list(sub_layout), **expandable(size=(1600, 1600), scroll_vertical=True))]
    return [layout, sub_layout]
prompt_tabs = get_prompt_tabs({"instructions": get_instructions(), "chunks": get_chunked_sections()}, args={**expandable(size=(75, None))})

def get_total_layout():
    prompt_tabs= get_prompt_tabs({"instructions":get_instructions(),"chunks":get_chunked_sections()},args={**expandable(size=(int(0.4*window_width),int(window_height)))})
    return [
        [get_progress_frame()],
        [get_output_options()],
        [get_column([[prompt_tabs]]),get_column(utilities())]
        ]
