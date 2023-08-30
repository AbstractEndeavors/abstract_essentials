from abstract_utilities.time_utils import get_current_year
from abstract_utilities.string_clean import eatAll
from abstract_utilities.path_utils import mkdirs,get_base_name,get_directory
from abstract_utilities.read_write_utils import write_to_file,read_from_file
from module_utils import get_installed_versions,scan_folder_for_required_modules
from abstract_gui import *
import datetime
import os
import json
create_folder_window_mgr,folder_bridge,create_folder_script = create_window_manager(script_name='create_folder_script',global_var=globals())
folder_bridge=folder_bridge.return_global_variables(script_name=create_folder_script)
folder_bridge["MODULE_FOLDER"]=None
folder_bridge["MODULE_NAV_HISTORY"] = []
folder_bridge["folder"] = os.getcwd()
import setuptools
import os
def make_columns(columns,layout,current_row,obj,num,max_num,last_bool:bool=False):
    num +=1
    current_row.append(obj)
    if (num) % columns == 0:  # +1 because index starts from 0
        layout.append(current_row)
        current_row = []

    # If there are remaining checkboxes that didn't make a full row of 3, add them
    if last_bool or num == max_num:
        layout.append(current_row)
    return num,current_row,layout
def return_largest_size(js,var):
    highest=0
    for each in js[var]:
        if len(each)>highest:
            highest=len(each)
    return highest
def new_layout(string:str,i):
    lay = [get_gui_fun('Combo',args={"values":get_dev_status_js()[string],"value":get_dev_status_js()[string][0],"size":(return_largest_size(get_dev_status_js(),string),1),"key":"-DEV_STATUS_"+string+str(i)+'-',"enable_events":True})]
    if string == "Programming Language":
        lay.append(get_gui_fun('Input',args={"default_text":"","key":"-VERSION_PY"+str(i)+"-","size":(5,1)}))
    return [lay]

def capture_setup(**kwargs):
    global setup_data
    setup_data = kwargs

def parse_setup(file_path: str = None):
    os.chdir(get_directory(file_path))
    original_setup = setuptools.setup
    setuptools.setup = capture_setup

    with open('setup.py', 'r') as f:
        setup_script = f.read()

    setup_data = {}
    exec(setup_script, {'setuptools': setuptools})

    keys_to_extract = ['name', 'version', 'author', 'author_email', 'description', 'url', 'classifiers']

    for key in keys_to_extract:
        value = setup_data.get(key)
        if value:
            print(f"{key}: {value}")
    return setup_data

def capture_setup_(**kwargs):
        return kwargs
def parse_setup(file_path:str=None):

    
    lines = read_from_file(file_path).split('\n')
    for line_num,each in enumerate(lines):
        line = eatAll(each,['',' ','\n','\t'])
        split_line = line.split('=')
        if split_line[0] in ['name','version','author','author_email','description','url','classifiers']:
            if split_line[0] in ['version','classifiers']:
                if split_line[0] == 'version':
                    value = line[len(split_line[0])+1:]
                    if ',' == value[-1]:
                        value = value[:-1]
                    for i,vers in enumerate(value.split('.')):
                        update_values(split_line[0]+'_'+str(i),{"value":eatAll(vers,['"',"'",'',' ','\n','\t',',','[',']'])})
                elif split_line[0] in 'classifiers':
                    keys = list(get_dev_status_js().keys())
                    classifiers=[line[len(split_line[0])+1:]]
                    for each in lines[line_num+1:]:
                        if '=' not in each:
                            classifiers.append(eatAll(each,['"',"'",'',' ','\n','\t',',','[',']']))
                        else:
                            break
                    have = []
                    for classifier in classifiers:
                         spl = classifier.split(' :: ')
                         key = eatAll(spl[0],['"',"'",'',' ','\n','\t',',','[',']'])
                         if key in keys:
                             replace_key = "-DEV_STATUS_"+key+'-'
                             version = "-VERSION_PY-"
                             if key in have:
                                 
                                 count = 0
                                 for i in range(len(have)):
                                     if have[i] == key:
                                         count +=1
                                 version ="-VERSION_PY"+str(count)+"-"
                                 replace_key = "-DEV_STATUS_"+key+str(count)+'-'
                                 if replace_key not in get_values():
                                     folder_bridge["window"].extend_layout(folder_bridge["window"]["-COLUMN"+"_"+key+"-"], new_layout(key,count))
                             have.append(key)
                             update_values(replace_key ,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']'])})
                             if "Programming Language" == key:
                                 update_values(replace_key ,{"value":eatAll(spl[1],['"',"'",'',' ','\n','\t',',','[',']'])})
                                 update_values(version,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']'])})
                             if "Development Status" == key:
                                update_values(replace_key ,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']']).split('- ')[-1]})
                             
            else:   
                value = line[len(split_line[0])+1:]
                if ',' == value[-1]:
                    value = value[:-1]
                
                update_values(split_line[0] ,{"value":eatAll(value,['"',"'",'',' ','\n','\t',',','[',']'])})

def list_all_directories(root_folder):
    """
    Recursively list all directories starting from root_folder.
    """
    directories = []
    if os.path.isdir(root_folder):
        directories.append(root_folder)
        for child in os.listdir(root_folder):
            child_path = os.path.join(root_folder, child)
            directories.extend(list_all_directories(child_path))
    return directories
def generate_directory_map(root_folder):
    """
    Recursively generate a dictionary mapping of folder and its content.
    """
    directory_map = {}
    if os.path.isdir(root_folder):
        directory_map[root_folder] = [os.path.join(root_folder, child) for child in os.listdir(root_folder)]
        for child in directory_map[root_folder]:
            directory_map.update(generate_directory_map(child))
    return directory_map
def get_values():
    return create_folder_window_mgr.get_values(window=folder_bridge["window"])
def update_values(key,args):
    if key != None:
        create_folder_window_mgr.update_values(window=folder_bridge["window"],key=key,args=args)
def get_all_choice_tags() -> list:
    """
    Get a list of all available choice tags.

    Returns:
        list: A list of choice tags.
    """
    return ["package_name","version","author_name","author","author_email","url","description","long_description"]
def get_dev_status_js():
    return {
        "Development Status":["Planning","Pre-Alpha","Alpha","Beta","Production/Stable","Mature","Inactive"],
        "Intended Audience":["Developers","End Users/Desktop","System Administrators","Science/Research","Education","Financial and Insurance Industry","Healthcare Industry","Information Technology"],
        "License":["MIT License","Apache Software License","GNU General Public License (GPL)","BSD License","Mozilla Public License (MPL)","Creative Commons Licenses","Proprietary/Closed Source","Public Domain"],
        "Operating System":["OS Independent","Microsoft","MacOS","POSIX (Linux, Unix-like systems)","Android","iOS"],
        "Programming Language":["Python","Java","C++","JavaScript","Go","Ruby","PHP"],
        "Supported Platforms":["Windows","Linux","macOS","Web (Browser-based)","Mobile (Android, iOS)","Cross-platform"],
        "Topic":["Software Developmentf","Internet :: WWW/HTTP","Utilities","Data Science","Machine Learning","Artificial Intelligence","Game Development","Networking","Security","Graphics","Multimedia"],
        "Framework":["Django","Flask","React","Angular","TensorFlow","PyTorch","NumPy","SciPy"],
        "Keywords":["database","web","API","GUI","automation","testing","visualization","cryptography","natural language processing","robotics","cloud computing"]
        }
def create_dev_status():
    layout = []
    current_row=[]
    num = 0
    dev_status_json = get_dev_status_js()
    for each in dev_status_json.keys():
        dev_status_value = dev_status_json[each]
        
        if each=="Programming Language":
            lay = [get_gui_fun("Combo",args={"values":dev_status_value,"value":dev_status_value[0],"size":(9,1),"key":"-DEV_STATUS_"+each+'-',"enable_events":True})]
            lay.append(get_gui_fun('Input',args={"default_text":"version","key":"-VERSION_PY-","size":(4,1)}))
        else:
            lay = [get_gui_fun("Combo",args={"values":dev_status_value,"value":dev_status_value[0],"size":(15,1),"key":"-DEV_STATUS_"+each+'-',"enable_events":True})]
        lay.append(get_gui_fun("Button",args={"button_text":"+","key":"-DEV_STATUS_"+each+"_BUTTON-","enable_events":True}))
        num,current_row,layout=make_columns(columns=3,
                                            layout=layout,current_row=current_row,obj=get_gui_fun("Frame",args={"title":each,"layout":ensure_nested_list(lay),"key":"-COLUMN"+"_"+each+"-"}),num=num,max_num=len(dev_status_json.keys()))
    return  get_gui_fun("Frame",args={"title":"Choose Dev Status","layout":ensure_nested_list(layout),"key":"-COLUMN-"
                                      ,"scrollable":True,"expand_x":False,"auto_scroll":True,"min_size":(200,200),**expandable()})
def create_toml() -> str:
    """
    Create the contents of a 'pyproject.toml' file.

    Returns:
        str: The contents of the 'pyproject.toml' file.
    """
    return f'''[build-system]
    requires = ["{get_installed_versions(['setuptools'])}"]
    build-backend = "setuptools.build_meta"'''
def create_check_marks() -> None:
    """
    Create a layout for checkboxes indicating files to be created.

    Returns:
        None
    """
    check_mark_layout = []
    current_row = []
    num = 0
    check_list = ['README.md', 'setup.cfg', 'project.toml', 'LICENSE', 'src_init', 'main.py', 'module_init', 'setup.py']
    for i, each in enumerate(check_list):
        check = get_gui_fun('Checkbox', args={"text": each, "default": True, "key": each, "enable_events": True})
        num,current_row,layout=make_columns(columns=2,
                                            layout=check_mark_layout,current_row=current_row,obj=check,num=num,max_num=len(check_list))
    return get_gui_fun("Frame",args={"title":"File Checklist","layout":ensure_nested_list(layout)})
def create_inputs(string: str) -> list:
    """
    Create layout elements for user inputs.

    Args:
        string (str): The input string to generate layout elements for.

    Returns:
        list: A list of layout elements for user inputs.
    """
    if string == "long_description":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Input',args={"default_text":os.getcwd(),"key":string}),
                get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]#[[get_gui_fun('T',{"text":string+':'})],[get_gui_fun('Input',args={"default":os.getcwd(),"key":string})],[get_gui_fun('FileBrowse', {"initial_folder":os.getcwd()})]]
    elif string == "version":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Input',args={"default_text":"0","key":string+'_0',"size":(2,1),"enable_events":True}),get_gui_fun('T',{"text":'.'}),
                get_gui_fun('Input',args={"default_text":"0","key":string+'_1',"size":(2,1),"enable_events":True}),
                get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_2',"size":(2,1),"enable_events":True}),
                get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_3',"size":(2,1),"enable_events":True})]
    elif string == "description":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Multiline',args={"key":string,"size":(None,None),"enable_events":True,**expandable()})]
    return [get_gui_fun('T',{"text":string+':'}),
            get_gui_fun('Input',args={"key":string,"size":(20,1),"enable_events":True})]
def create_choice_tag_layout():
    choice_tag_layout=[]
    choice_tags = get_all_choice_tags()
    for each in choice_tags:
        if each not in ["description","long_description"]:
            choice_tag_layout.append(create_inputs(string=each))
    return get_gui_fun("Frame",args={"title":"Choice Tags","layout":ensure_nested_list(choice_tag_layout)})
def get_descriptions_layout():
    description_layout=[]
    description_list = ["description","long_description"]
    for each in description_list:
        description_layout.append(create_inputs(string=each))
    return get_gui_fun("Frame",args={"title":"Descriptions","layout":ensure_nested_list(description_layout),**expandable()})
def get_module_folder_browser(initial_folder:str=os.getcwd()):

    return [ 
             get_gui_fun("Frame",args={"title":"Choose Module Directory","layout":ensure_nested_list([
                 get_gui_fun('Input',args={"default_text":initial_folder,"disabled":False,"key":"-MODULE_PERMENANT_PATH-","enable_events":True}),
                 get_gui_fun('Input',args={"default_text":initial_folder,"key":"-MODULE_FOLDER_PATH-","enable_events":True}),
                                                                                                     get_gui_fun('FolderBrowse', {"initial_folder": initial_folder,"key":"-MODULE_FOLDER_BROWSER-","enable_events":True}),
                                                                                                     get_gui_fun("Checkbox",args={"text":"choose folder","default":False,"key":"-LOCK_CHECKBOX-","enable_events":True})])})]
        

        


def get_all_choice_tags() -> list:
    """
    Get a list of all available choice tags.

    Returns:
        list: A list of choice tags.
    """
    return ["package_name","version","author_name","author","author_email","url","description","long_description"]
def check_all_files(directory:str):
    check_list = [ 'src_init', 'main.py', 'module_init', ]
    name = directory.split('/')[-1]
    update_values('package_name',{"value":name})
    for each in ['README.md', 'setup.cfg', 'project.toml', 'LICENSE','setup.py']:
        if each in os.listdir(directory):
            update_values(each,{"value":False,"disabled":True})
            if each == 'setup.py':
                input(parse_setup(os.path.join(directory,'setup.py')))
    src_folder = os.path.join(directory,"src")
    print(src_folder)
    if os.path.exists(src_folder):
        if '__init__.py' in os.listdir(src_folder):
            update_values('src_init',{"value":False,"disabled":True})
    module_folder = os.path.join(src_folder,name)
    print(module_folder)
    if os.path.exists(module_folder):
        checks = ['module_init','main.py']
        for i,each in enumerate(['__init__.py','main.py']):
            if each in os.listdir(module_folder):
                update_values(checks[i],{"value":False,"disabled":True})
def create_module_folder() -> str:
    """
    Create a new module folder and generate necessary files based on user input.

    Returns:
        str: The path of the created module folder.
    """
    for each in folder_bridge["topics_js"].keys():
        folder_bridge["classifiers_layout"].append(create_dropdown(each,folder_bridge["topics_js"][each]))
    folder_bridge["classifiers_layout"] = [get_gui_fun("Frame",args={"title":"classifiers","layout":folder_bridge["classifiers_layout"]})]
    for each in get_all_choice_tags():
        folder_bridge["sections_layout"].append(create_inputs(each))
    create_check_marks()
    folder_bridge["path_checked"] = False
    folder_bridge["sections_layout"] = [get_gui_fun("Frame",args={"title":"classifiers","layout":folder_bridge["sections_layout"]})]
    default_inputs_layout = [get_gui_fun("Frame",args={"title":"choose default inputs","layout":[[sg.Button("default_inputs_submit"),get_gui_fun('Input',args={"default_text":os.path.join(os.getcwd(),"default_inputs.json"),"key":"default_inputs"}), get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]]})]
    parent_folder_layout = [get_gui_fun("Frame",args={"title":"Parent Folder","layout":[[get_gui_fun('Input',args={"default_text":os.getcwd(),"key":"parent_folder"}), get_gui_fun('FolderBrowse', {"initial_folder": os.getcwd()})]]})]
    folder_bridge["check_mark_layout"] = [get_gui_fun("Frame",args={"title":"Files To Create","layout":ensure_nested_list(folder_bridge["check_mark_layout"])})]
    folder_bridge["license_layout"] = [get_gui_fun("Frame",args={"title":"license","layout":ensure_nested_list([get_gui_fun("Combo",args={"values":list(get_license_json().keys()),"default_value":list(get_license_json().keys())[0],"enable_events":True,"key":"-LICENSE-"})])})]
    layout = [[default_inputs_layout],[parent_folder_layout],[folder_bridge["sections_layout"],folder_bridge["license_layout"]],[folder_bridge["classifiers_layout"]],[folder_bridge["check_mark_layout"]]]
    window = create_folder_window_mgr.get_new_window(args={"title":'setup_window','layout':ensure_nested_list([layout,[sg.Button("Submit")]])},event_function="value_function",exit_events=["Submit"])
    create_folder_window_mgr.while_basic(window)
    write_files()
    write_to_file(filepath=os.path.join(parent_folder,"default_inputs.json"),contents=json.dumps(folder_bridge["type_choices"]))
    return folder_bridge["module_folder"]
def while_module(event):
    
    values = get_values()
    if "-DEV_STATUS_" in event and event[-len("_BUTTON-"):] == "_BUTTON-":
        i=0
        while event[:-len("_BUTTON-")]+str(i)+'-' in values:
            i+=1
        key = event[len("-DEV_STATUS_"):-len("_BUTTON-")]
        folder_bridge["window"].extend_layout(folder_bridge["window"]["-COLUMN"+"_"+key+"-"],new_layout(key,i))
    folder_contents={"parent":['README.md', 'setup.cfg', 'project.toml', 'LICENSE','setup.py'] , "src":['src_init'],"module":['main.py','module_init']}
    if event == "-CREATE_FOLDER-":
        new_folder_name = get_gui_fun('PopupGetText', {"message": "Enter the new folder name:"})
        if new_folder_name:
            folder_path = os.path.join(values["-MODULE_FOLDER_PATH-"], new_folder_name)
            os.makedirs(folder_path, exist_ok=True)
            update_values("-DIRECTORY_LIST-", {"values": os.listdir(folder_bridge["MODULE_FOLDER"])})
    elif event == "-DIRECTORY_LIST-":
        chosen_path = None
        if len(values["-DIRECTORY_LIST-"]) != 0:
            chosen_folder = values["-DIRECTORY_LIST-"][0]  # This retrieves the selected folder from the listbox
            if values["-MODULE_FOLDER_PATH-"] != None:
                chosen_path = os.path.join(values["-MODULE_FOLDER_PATH-"], chosen_folder)
            if chosen_path != None:
                if os.path.isdir(chosen_path):  # This checks if the selected item is a directory
                    update_values("-MODULE_FOLDER_PATH-", {"value":chosen_path})
                    update_values("-DIRECTORY_LIST-", {"values": os.listdir(chosen_path)})
                    if not values["-LOCK_CHECKBOX-"]:
                        update_values("-MODULE_PERMENANT_PATH-",{"value":chosen_path})
            else:
                create_folder_window_mgr.while_basic(create_folder_window_mgr.get_new_window(title="warning",layout=[[get_gui_fun('T', {"text": f"{chosen_folder} is not a directory."})],create_row_of_buttons("OK")],exit_events=["OK"]))
    if event == "-LOCK_CHECKBOX-":
        if not values["-LOCK_CHECKBOX-"]:
            #folder_bridge["window"]["-MODULE_PERMENANT_PATH-"].update(disabled=True)
            update_values("-MODULE_PERMENANT_PATH-",{"disabled":False})
            folder_bridge["MODULE_FOLDER"] = None
        elif values["-LOCK_CHECKBOX-"]:
            update_values("-MODULE_PERMENANT_PATH-",{"value":values["-MODULE_FOLDER_PATH-"]})
            update_values("-MODULE_PERMENANT_PATH-",{"disabled":True})
            folder_bridge["MODULE_FOLDER"]=values["-MODULE_PERMENANT_PATH-"]
            check_all_files(folder_bridge["MODULE_FOLDER"])
        
             
    if event in ["-MODULE_FOLDER_PATH-","-MODULE_FOLDER_BROWSER-"]:
        if os.path.exists(values["-MODULE_FOLDER_PATH-"]):
            update_values("-DIRECTORY_LIST-", {"values": os.listdir(values["-MODULE_FOLDER_PATH-"])})
            folder = values["-MODULE_FOLDER_PATH-"]  # fetch the folder path
            if folder:
                update_values("-MODULE_FOLDER_PATH-", {"value":folder})  # update the input text with the folder path
            
                if not values["-LOCK_CHECKBOX-"]:
                    update_values("-MODULE_PERMENANT_PATH-", {"value":folder})  # if not locked, update the permanent directory input text too
    elif event == '<-':
        current_folder = values["-MODULE_FOLDER_PATH-"]
        parent_folder = os.path.dirname(current_folder) if current_folder else None
        if folder_bridge["MODULE_FOLDER"] != None:
            if parent_folder in list_all_directories(folder_bridge["MODULE_FOLDER"]):
                update_values("-MODULE_FOLDER_PATH-", {"value": parent_folder})
                update_values("-DIRECTORY_LIST-", {"values": os.listdir(parent_folder)})
        
        elif parent_folder and os.path.exists(parent_folder):
            update_values("-MODULE_FOLDER_PATH-", {"value": parent_folder})
            update_values("-DIRECTORY_LIST-", {"values": os.listdir(parent_folder)})
            
            # Add current folder to history
            folder_bridge["MODULE_NAV_HISTORY"].append(current_folder)
        
    elif event == '->':
        if folder_bridge["MODULE_NAV_HISTORY"]:
                next_folder = folder_bridge["MODULE_NAV_HISTORY"].pop()
                if folder_bridge["MODULE_FOLDER"] != None:
                    all_directories = list_all_directories(folder_bridge["MODULE_FOLDER"])
                    all_directories.append(folder_bridge["MODULE_FOLDER"])
                    if next_folder in all_directories:
                        update_values("-MODULE_FOLDER_PATH-", {"value": next_folder})
                        update_values("-DIRECTORY_LIST-", {"values": os.listdir(next_folder)})
            
                
                elif os.path.exists(next_folder):
                    #folder_bridge["MODULE_FOLDER"] = next_folder
                    update_values("-MODULE_FOLDER_PATH-", {"value": next_folder})
                    update_values("-DIRECTORY_LIST-", {"values": os.listdir(next_folder)})
def get_layout():
    listbox= [[]]
    
    folder_bridge["window"] = create_folder_window_mgr.get_new_window("create module",
                                                     args={'layout':[[
                                                         get_gui_fun("Listbox", args={"values": os.listdir(os.getcwd()), "size": (20, 20), "key": "-DIRECTORY_LIST-", "bind_return_key": True, "enable_events": True}),
                                                         create_row_of_buttons('<-','->'),
                                                         create_check_marks(),
                                                         get_descriptions_layout(),get_module_folder_browser()],
                                                         [create_dev_status(),[]]],"event_function":"while_module",**expandable()})
    create_folder_window_mgr.while_basic(folder_bridge["window"])
def get_layout2():
    listbox= get_gui_fun("Listbox", args={"values": os.listdir(os.getcwd()), "size": (20, 20), "key": "-DIRECTORY_LIST-", "bind_return_key": True, "enable_events": True})
    buttons = create_row_of_buttons('<-','->')
    listbox_column = sg.Column([[listbox],buttons])
    check_marks_column = sg.Column([[create_check_marks()],[create_choice_tag_layout()]])
    status_column = sg.Column([[create_check_marks(),create_choice_tag_layout()],[create_dev_status()]])
    top_frame =get_gui_fun("Frame",args={"title":"","layout":[[listbox_column,status_column],get_module_folder_browser()]})
    folder_bridge["window"] = create_folder_window_mgr.get_new_window("create module",
                                                     args={'layout':[[get_descriptions_layout(),[top_frame]
                                                        ]],"event_function":"while_module","min_size":(500,500),"max_size":(1000,1000),"resizable":True, "pad":(0,0)})
    create_folder_window_mgr.while_basic(folder_bridge["window"])

get_layout2()
