"""
abstract_rpcs.py
=================================================================================
This module provides an interface to choose and manage RPC parameters for a blockchain.
It enables the user to filter and select various RPC parameters via a GUI interface.
"""
import json
from abstract_utilities.read_write_utils import read_from_file
from abstract_gui import create_window_manager,get_gui_fun,create_row_of_buttons,sg
window_mgr,rpc_global_bridge,rpc_add_script_name=create_window_manager(global_var=globals())
rpc_add_global_bridge=rpc_global_bridge.return_global_variables(rpc_add_script_name)
def win_while(event:str):
    """
    Event loop function for the GUI window. 
    It updates the GUI window elements based on the user interactions with the various components.
    
    Parameters:
    - event (str): The name of the GUI component that was interacted with.
    """
    event,values,window = window_mgr.get_event(),window_mgr.get_values(),window_mgr.get_last_window_method()
    if event == "-BLOCK_EXPLORER-":
        window_mgr.update_values(window=window, key=event[:-1]+'_CHECK-', args={"value":True})
        rpc_add_global_bridge["check_list"][event] = ''
        for each in list(get_js().values()):
            if each != event:
                rpc_add_global_bridge["check_list"][each] = ''
                window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)]})
                window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
            # Reset filters
        if each != event:
            rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
            keyed_rpc_lists()
            filter_list()
            window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)], "value":''})
            window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
    if event == 'reset':
        # Clear the check list
        for each in list(get_js().values()):
            rpc_add_global_bridge["check_list"][each] = ''
            window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)]})
            window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
        # Reset filters
        rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
        keyed_rpc_lists()
        filter_list()
        window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)], "value":''})
        window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
    elif event in list(get_js().values()):
        rpc_add_global_bridge["check_list"][event] =window_mgr.get_values()[event]
        window_mgr.update_values(window=window,key=event[:-1]+'_CHECK-',args={"value":True})
    elif '_CHECK-' in event:
        if values[event] == False:
            window_mgr.update_values(window=window,key=event,args={"value":False})
            rpc_add_global_bridge["check_list"][event[:-len('_CHECK-')]+'-'] = ''
    filter_list()
def filter_rpc_list_by_selections()->list:
    """
    Filters the RPC list based on the user's selections in the GUI window.
    
    Returns:
    - list: A filtered list of RPCs.
    """
    # Start with the full list of RPCs
    rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
    event,values = window_mgr.get_event(),window_mgr.get_values()
    # For each key in the selection values, filter the list if the key's value is set
    rpc_list=[]
    for rpc in rpc_add_global_bridge["recursed_rpc_js_list"]:
        bool_list,bool_count = [],0
        for rpc_key, event_key in get_js().items():
            event_check = event_key[:-1]+'_CHECK-'
            if values[event_check] == True:
                bool_count +=1
                static = values[event_key]
                if rpc_key in rpc:
                    if static == rpc[rpc_key]:
                        bool_list.append(rpc[rpc_key])
        if bool_count == len(bool_list):
            rpc_list.append(rpc)
    return rpc_list
def filter_list()->None:
    """
    Updates the GUI dropdown lists based on the filtered RPC list.
    """
    # Get the filtered list of RPCs based on current selections
    rpc_add_global_bridge["recursive_filtered_list"] = filter_rpc_list_by_selections()
    event,values = window_mgr.get_event(),window_mgr.get_values()
    # Update each dropdown using the filtered list
    for rpc in rpc_add_global_bridge["recursive_filtered_list"]:
        for key in get_keys():
            unique_values=[]
            if key in rpc:
                if rpc[key] not in unique_values:
                    unique_values.append(rpc[key])
            if get_js()[key] in rpc_add_global_bridge["check_list"][get_js()[key]]:
                value = rpc_add_global_bridge["check_list"][get_js()[key]]
            elif  key == 'blockExplorer':
                unique_values = rpc_add_global_bridge["blockExplorers"]
            else:
                if len(unique_values)>=1:
                    value = unique_values[0]
                else:
                    value = None
            window_mgr.update_values(window= window_mgr.get_last_window_method(),key=get_js()[key],args={"values":unique_values,"value":value})
def keyed_rpc_lists(event:str=None)->None:
    """
    Organizes the RPC list into sub-lists based on keys.
    
    Parameters:
    - event (str, optional): Event triggered in the GUI. Defaults to None.
    """
    rpc_add_global_bridge["keyed_lists"]={}
    for each in list(get_js().keys()):
        rpc_add_global_bridge["keyed_lists"][each]=[]
        for i,each_js in enumerate(rpc_add_global_bridge["recursed_rpc_js_list"]):
            if each in each_js:
                if each_js[each] not in rpc_add_global_bridge["keyed_lists"][each]:
                    rpc_add_global_bridge["keyed_lists"][each].append(each_js[each])

def get_key_from_value(value:str)-> (str or None):
    """
    Fetches the key for a given value from the `get_js()` mapping.
    
    Parameters:
    - value: The value for which the key needs to be found.
    
    Returns:
    - The key corresponding to the value.
    """
    for i,each in enumerate(get_js().values()):
        if value == each:
            return get_keys()[i]
def get_js()->dict:
    """
    Provides a dictionary mapping of RPC parameters.
    
    Returns:
    - dict: A dictionary of RPC parameters.
    """
    return {"netName":"-NETWORK_NAME-",'network':"-NETWORK-",'nativeCurrency':"-NATIVE_CURRENTY-",'chainId':"-CHAIN_ID-",'RPC':"-RPC-",'blockExplorer':"-BLOCK_EXPLORER-"}
def get_keys()->list:
    """
    Fetches the keys from the `get_js()` mapping.
    
    Returns:
    - list: A list of keys.
    """
    return list(get_js().keys())
def get_values():
    """
    Fetches the values from the `get_js()` mapping.
    
    Returns:
    - list: A list of values.
    """
    return list(get_js().values())
def push()-> get_gui_fun("Push"):
    """
    Fetches the "Push" function from the GUI module.
    
    Returns:
    - function: The "Push" GUI function.
    """
    return get_gui_fun("Push")

def get_rpc_list()->(list or dict):
    """
    Reads and returns the RPC list from a JSON file.
    
    Returns:
    - list: The RPC list.
    """
    return json.loads(read_from_file('data/rpcListNew.json'))
def Choose_RPC_Parameters_GUI(RPC_list:list=None) -> dict or None:
    """
    Creates and launches the GUI window for selecting RPC parameters.
    
    Parameters:
    - RPC_list (list, optional): The list of RPC parameters. If not provided, it will fetch the default list.
    
    Returns:
    - dict: A dictionary containing the selected RPC parameters.
    """
    if RPC_list == None:
        RPC_list = get_rpc_list()
    rpc_add_global_bridge["get_rpc_list"] = RPC_list
    rpc_add_global_bridge["total_bool_list"] = []
    rpc_add_global_bridge["recursed_rpc_js_list"]=get_rpc_list()
    rpc_add_global_bridge["check_list"]={}
    for each in list(get_js().values()):
        rpc_add_global_bridge["check_list"][each] = ''
    keyed_rpc_lists(get_rpc_list())
    rpc_add_global_bridge["blockExplorers"]=rpc_add_global_bridge["keyed_lists"]["blockExplorer"]
    layout = [
        [get_gui_fun("Text",args={"text":"Block Explorer"}),
         get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"]["blockExplorer"],"default_text":rpc_add_global_bridge["keyed_lists"]["blockExplorer"][0],
                                   "key":"-BLOCK_EXPLORER-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-BLOCK_EXPLORER_CHECK-"}),
         push()],
        [get_gui_fun("Text",args={"text":"Network"}),
         get_gui_fun("Combo",args={"values":["Mainnet","TestNet"],
                                   "default_value":"Mainnet",
                                   "key":"-NETWORK-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-NETWORK_CHECK-"}),
         push()],
        [get_gui_fun("Text",args={"text":"Native Currency"}),
         get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"]["nativeCurrency"],"default_text":rpc_add_global_bridge["keyed_lists"]["nativeCurrency"][0],
                                   "key":"-NATIVE_CURRENTY-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-NATIVE_CURRENTY_CHECK-"}),
         push()],
        [get_gui_fun("Text",args={"text":"Chain Id"}),
         get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"]["chainId"],"default_text":rpc_add_global_bridge["keyed_lists"]["chainId"][0],
                                   "key":"-CHAIN_ID-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-CHAIN_ID_CHECK-"}),
         push()],
        [get_gui_fun("Text",args={"text":"RPC"}),
         get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"]["RPC"],"default_text":rpc_add_global_bridge["keyed_lists"]["RPC"][0],
                                   "key":"-RPC-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-RPC_CHECK-"}),
         push()],
        [get_gui_fun("Text",args={"text":"Network Name"}),
         get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"]["netName"],"default_text":rpc_add_global_bridge["keyed_lists"]["netName"][0],
                                   "key":"-NETWORK_NAME-","enable_events":True}),
         get_gui_fun("Checkbox",args={"text":"","default_value":False,"key":"-NETWORK_NAME_CHECK-"}),
         push()],
        ]
    menu_def = [['File',  'Save', 'Exit',],['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],['Help', 'About...'],]
    layout = [[sg.Menu(menu_def)],layout,[create_row_of_buttons("OK","Show","reset","Exit"),]]
    window = window_mgr.get_new_window(args={"title":'ADD RPC',"layout":layout,"exit_events":["OK","Exit"],"event_function":"win_while","suppress_raise_key_errors":False, "suppress_error_popups":False, "suppress_key_guessing":False,"finalize":True})
    values = window_mgr.while_basic(window=window)
    rpc = {}
    for each in get_values():
        rpc[get_key_from_value(each)] = values[each]
    return rpc



