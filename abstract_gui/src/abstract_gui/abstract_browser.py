"""
abstract_browser
=================

The `abstract_browser` module is part of the `abstract_gui` module of the `abstract_essentials` package. 
It provides an abstracted mechanism for creating and managing a file/folder browser using PySimpleGUI.

Classes and Functions:
----------------------
- get_scan_browser_layout: Returns the layout for the file/folder scanner window.
- browse_update: Updates values in the browse window.
- return_directory: Returns the current directory or parent directory if a file is selected.
- scan_window: Handles events for the file/folder scanner window.
- forward_dir: Navigate to the given directory.
- scan_directory: Returns the files or folders present in the given directory based on the selected mode.
- get_browse_scan: Initializes the scanner with default settings and runs it.

"""
import os
from abstract_gui import create_window_manager,get_gui_fun,create_row_of_buttons,get_yes_no
from abstract_utilities.path_utils import get_directory,is_file,dir_exists,get_base_name,get_directory
def get_scan_browser_layout():
    """
    Generate the layout for the file/folder scanning window.

    Returns:
    --------
    list:
        A list of list of PySimpleGUI elements defining the window layout.
    """
    return [
        [get_gui_fun("Text",args={"text":'Directory to scan:'}), get_gui_fun("InputText",args={"default_text":os.getcwd(),"key":'-DIR-'}),
         get_gui_fun("FolderBrowse",args={"button_text":"Folders", "enable_events":True, "key":"directory"}),
         get_gui_fun("FileBrowse",args={"button_text":"Files", "enable_events":True, "key":"files"})],
        [get_gui_fun("Listbox",args={"values":[],"size":(50, 10),"key":'-FILES-',"enable_events":True})],
        [create_row_of_buttons({"button_text":"Scan","key":"-SCAN-","enable_events":True},"<-",{"button_text":"File Scan Mode","key":"-MODE-","enable_events":True},"->",'Select Highlighted','Ok')]
    ]
window_browser_mgr,browse_bridge,browse_script_name=create_window_manager(script_name="browse_script",global_var=globals())
js_browse_bridge = browse_bridge.return_global_variables(script_name=browse_script_name)
js_browse_bridge["browse_window"] = window_browser_mgr.get_new_window('File/Folder Scanner',args={"layout":get_scan_browser_layout(),"exit_events":["Ok","OK"],"event_function":"scan_window"})    
def browse_update(window=js_browse_bridge["browse_window"], key: str = None, args: dict = {}):
    """
    Update specific elements in the browse window.

    Parameters:
    -----------
    window : PySimpleGUI.Window
        The window to be updated. Default is the global `browse_window`.
    key : str, optional
        The key of the window element to update.
    args : dict, optional
        Arguments to be passed for the update operation.
    """
    window_browser_mgr.update_values(window=js_browse_bridge["browse_window"],key=key,args=args)
def return_directory():
    """
    Return the current directory or parent directory if a file path is provided.

    Returns:
    --------
    str:
        Directory path.
    """
    values = window_browser_mgr.get_values()
    directory = values['-DIR-']
    if is_file(values['-DIR-']):
        directory = get_directory(values['-DIR-'])
    if directory == '':
        directory = os.getcwd()
    return directory
def scan_window(event):
    """
    Event handler function for the file/folder scanning window.

    Parameters:
    -----------
    event : str
        Name of the event triggered in the window.
    """
        
    values = window_browser_mgr.get_values()
    if event == "files":
        browse_update(key='-DIR-',args={"value":values["files"]})
    if event == "directory":
        browse_update(key='-DIR-',args={"value":values["directory"]})
    if event == '-SCAN-':
        js_browse_bridge["last_scan"]=is_file(values['-DIR-'])
        scan_results = scan_directory(return_directory(), js_browse_bridge["scan_mode"])
        browse_update(key='-FILES-',args={"values":scan_results})
    if event == 'Select Highlighted':
        if len(values['-FILES-'])>0:
            browse_update(key='-DIR-',args={"value":os.path.join(return_directory(), values['-FILES-'][0])})
    if event == '-MODE-':
        js_browse_bridge["scan_mode"] = 'folder' if js_browse_bridge["scan_mode"] == 'file' else 'file'
        js_browse_bridge["browse_window"].Element('-MODE-').update(text=f"F{js_browse_bridge['scan_mode'][1:]}  Scan Mode")

    if event == "<-":
        # Navigate up to the parent directory
        if return_directory() not in js_browse_bridge["history"]:
            js_browse_bridge["history"].append(return_directory())
        directory = os.path.dirname(return_directory())  # This will give the parent directory
        browse_update(key='-DIR-',args={"value":directory})
        browse_update(key='-FILES-',args={"values":scan_directory(directory, js_browse_bridge["scan_mode"])})
    if event == "->":
        # Navigate down into the selected directory or move to the next history path
        if values['-FILES-']:  # If there's a selected folder in the listbox
            directory = os.path.join(return_directory(), values['-FILES-'][0])
            forward_dir(directory)
        elif js_browse_bridge["history"]:  # If there's a directory in the history stack
            directory = js_browse_bridge["history"].pop()
            browse_update(key='-DIR-',args={"value":directory})
            browse_update(key='-FILES-',args={"values":scan_directory(directory, js_browse_bridge["scan_mode"])})
def forward_dir(directory):
    """
    Navigate and update the scanner to display contents of the given directory.

    Parameters:
    -----------
    directory : str
        Path to the directory to navigate to.
    """
    if os.path.isdir(directory):
        browse_update(key='-DIR-',args={"value":directory})
        browse_update(key='-FILES-',args={"values":scan_directory(directory, js_browse_bridge["scan_mode"])})
def scan_directory(directory_path, mode):
    """
    List files or folders in the given directory based on the provided mode.

    Parameters:
    -----------
    directory_path : str
        Path to the directory to scan.
    mode : str
        Either 'file' or 'folder' to specify what to list.

    Returns:
    --------
    list:
        List of file/folder names present in the directory.
    """
    if mode == 'file':
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    else: # mode == 'folder'
        return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    return browse_bridge['-DIR-']
def get_browse_scan():
    """
    Initialize and run the file/folder scanner window with default settings.

    Returns:
    --------
    str:
        The path selected in the scanner.
    """
    js_browse_bridge["scan_mode"]="file"
    js_browse_bridge["history"] = []
    return window_browser_mgr.while_basic(window=js_browse_bridge["browse_window"])["-DIR-"]
def popup_T_F(title:str="popup window",text:str="popup window text"):
    answer = get_yes_no(title=title,text=text)
    if answer == "Yes":
        return True
    return False
def create_new_entity(event:str=None, entity_type:str="Folder"):
    # Retrieve values from the GUI
    values = window_browser_mgr.get_values(window=window_browser_mgr.get_last_window_method())
    if "-ENTITY_TYPE-" in values:
        entity_type = values["-ENTITY_TYPE-"]
    if event in ["-FOLDER_BROWSE-",'-ENTITY_NAME-']:
        if os.path.isfile(values['-ENTITY_NAME-']):
            window_browser_mgr.update_values(window=window_browser_mgr.get_last_window_method(),key="-PARENT_DIR-",args={"value":get_directory(values['-ENTITY_NAME-'])})
            file_name = get_base_name(values['-ENTITY_NAME-'])
            window_browser_mgr.update_values(window=window_browser_mgr.get_last_window_method(),key='-ENTITY_NAME-',args={"value":file_name})
    if event == "Create":
        exists =False
        if values['-ENTITY_NAME-'] and values['-PARENT_DIR-']:
            entity_path = os.path.join(values['-PARENT_DIR-'],values['-ENTITY_NAME-'])
            if entity_type == "Folder":
                exists = os.path.exists(entity_path)  # changed from os.path.dir_exists(entity_path)
            if entity_type == "File":
                exists = os.path.exists(entity_path)
            if exists:
                if not popup_T_F(title=f"Override the {entity_type}?",text=f"looks like the {entity_type} path {entity_path} already exists\n did you want to overwrite it?"):
                    return False
            if entity_type == "Folder" and not exists:
                os.makedirs(entity_path, exist_ok=True)
            elif entity_type == "File":
                with open(entity_path, 'w') as f:
                    if "save_data" in js_browse_bridge:
                        f.write(js_browse_bridge["save_data"])  # writes the save_data to the file
                    else:
                        pass  # creates an empty file, or you can handle this differently
            window_browser_mgr.update_values(window=window_browser_mgr.get_last_window_method(),key="-FINAL_OUTPUT-",args={"value":entity_path})
            window_browser_mgr.update_values(window=window_browser_mgr.get_last_window_method(),key="-SAVE_PROMPT-",args={"visible":True})
            window_browser_mgr.get_last_window_method().Element("Cancel").update(text="Exit")

            return "Cancel"
            
def save_entity(initial_folder:str=os.getcwd(), entity_type:str="Folder",entity_name:str="",default_prompt:str='Enter the new folder name:',save_data:any=None):
    file_browser_visible = False
    saved_prompt = "Folder Created!!"
    if save_data:
        js_browse_bridge["save_data"] = save_data
        entity_type = "File"
    if entity_type == "File":
        saved_prompt = "File Saved!!"
        if default_prompt == 'Enter the new folder name:':
            default_prompt = 'Enter the new file name or choose from File Browser:'
        file_browser_visible = True
    layout = [
        [get_gui_fun("Text", args={"text": default_prompt})],
        [get_gui_fun("Input", args={"default_text":entity_name,"key": '-ENTITY_NAME-',"enable_events":True}),get_gui_fun("FileBrowse", args={"button_text":"File Browse","key":"-FOLDER_BROWSE-","initial_folder": initial_folder,"enable_events":True,"visible":file_browser_visible})],
        [get_gui_fun("Text", args={"text": 'Select Parent Directory:'})],
        [get_gui_fun("Input", args={"default_text": initial_folder, "key": "-PARENT_DIR-", "disabled": True,"enable_events":True}), 
         get_gui_fun("FolderBrowse", args={"button_text":"Dir Browse","key":"-DIRECTORY_BROWSE-","initial_folder": initial_folder,"enable_events":True})],
        [create_row_of_buttons('Create', {"button_text":'Cancel',"key":"Cancel","enable_events":True}),get_gui_fun("Push"),get_gui_fun("Input", args={"disabled":True,"default_text":entity_type,"key":"-ENTITY_TYPE-","size":(len(entity_type),1)}),get_gui_fun("Input", args={"default_text":"","key":"-FINAL_OUTPUT-","visible":False})],
        [get_gui_fun("Text", args={"text": saved_prompt,"key":"-SAVE_PROMPT-","visible":False})]
    ]
    window = window_browser_mgr.get_new_window(args={"layout": layout, "title": f"Create New {entity_type}", "event_function": "create_new_entity", "exit_events": ["Exit","Cancel"]})
    entity_name = window_browser_mgr.while_basic(window=window
    )
    return window_browser_mgr.all_windows[window_browser_mgr.search_global_windows(window)]["values"]['-FINAL_OUTPUT-']
get_browse_scan()
