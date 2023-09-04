"""
abstract_rpcs.py - RPCData and GUI Module

This module provides an interface to choose and manage RPC parameters for a blockchain.
It enables the user to filter and select various RPC parameters via a GUI interface.

Classes:
    RPCData: A class to manage RPC parameters for a blockchain.

Functions:
    win_while: Event loop function for the GUI window.
    filter_rpc_list_by_selections: Filters the RPC list based on user selections.
    keyed_rpc_lists: Organizes the RPC list into sub-lists based on keys.
    get_key_from_value: Fetches the key for a given value from the `get_js()` mapping.
    get_js: Provides a dictionary mapping of RPC parameters.
    get_keys: Fetches the keys from the `get_js()` mapping.
    get_values: Fetches the values from the `get_js()` mapping.
    get_default_rpc_list: Retrieves the default RPC list.
    get_rpc_list: Reads and returns the RPC list from a JSON file.
    save_rpc_list: Saves the RPC list to a JSON file.
    Choose_RPC_Parameters_GUI: Creates and launches the GUI window for selecting RPC parameters.
"""
import os
from abstract_utilities.json_utils import load_from_file,dump_to_file
from abstract_utilities.list_utils import filter_json_list_values,recursive_json_list
from abstract_gui import create_window_manager,get_gui_fun,create_row_of_buttons,get_menu,get_push
from web3 import Web3
window_mgr,rpc_global_bridge,rpc_add_script_name=create_window_manager(global_var=globals())
rpc_add_global_bridge=rpc_global_bridge.return_global_variables(rpc_add_script_name)
class RPCData:
    """
    RPCData class manages RPC parameters for a blockchain.
    """
    def __init__(self, rpc_js):
        """
        Initializes the RPCData instance with RPC parameters.

        :param rpc_js: Dictionary containing RPC parameters.
        """
        self.rpc_js = self.categorize_rpc_items(rpc_js)
        self.symbol = self.rpc_js['Symbol']
        self.network_name = self.rpc_js['Network_Name']
        self.block_explorer = self.rpc_js['Block_Explorer']
        self.rpc = self.rpc_js['RPC']
        self.chain_id = self.rpc_js['ChainID']
        self.scanner = self.strip_web(self.block_explorer)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
        
    @staticmethod
    def categorize_rpc_items(rpc_js):
        categorization = {
            "Network": "",
            "RPC": "",
            "Block_Explorer": "",
            "ChainID": "",
            "Symbol": "",
            "Network_Name": ""
        }
        for key in categorization.keys():
            if key not in rpc_js:
                rpc_js[key]=""
        url_candidates = []
        string_items = []

        for key, value in rpc_js.items():
            # Check Network
            if value.upper() in ['MAINNET', 'TESTNET']:
                categorization["Network"] = value
                continue
            
            # Check for urls
            stripped_value = RPCData.strip_web(value)
            if len(value) != len(stripped_value):
                url_candidates.append(value)  # Keep the original URL
                continue
            # Remaining items go to string items list
            string_items.append(value)
        
        # Classify URLs
        url_candidates = sorted(url_candidates, key=lambda x: (x.startswith('http://rpc') or x.startswith('https://rpc'), 'rpc' in x, -RPCData.count_slashes(x)), reverse=True)
        if len(url_candidates)>0:
            categorization["RPC"] = url_candidates[0]
        if len(url_candidates)>1:
            categorization["Block_Explorer"] = url_candidates[1]
        if len(categorization["Block_Explorer"]) > len(categorization["RPC"]):
            rpc=categorization["RPC"]
            categorization["RPC"]=categorization["Block_Explorer"]
            categorization["Block_Explorer"]=rpc
        # Classify ChainID
        string_items = sorted(string_items, key=lambda x: -RPCData.percent_integer_of_string(x))
        categorization["ChainID"] = string_items.pop(0)

        # Classify Network_Name and Symbol
        string_items = sorted(string_items, key=len)
        categorization["Symbol"] = string_items[0]
        if len(string_items) > 1:
            categorization["Network_Name"] = string_items[1]
                
        return categorization
    
    @staticmethod
    def strip_web(url:str):
        if url.startswith("http://"):
            url = url.replace("http://", '', 1)
        elif url.startswith("https://"):
            url = url.replace("https://", '', 1)
        url = url.split('/')[0]
        return url

    @staticmethod
    def count_slashes(s):
        return s.count('/')

    @staticmethod
    def percent_integer_of_string(s):
        if len(s) == 0:
            return 0
        return sum(c.isdigit() for c in s) / len(s)
    
    def return_rpc_js(self):
        return self.rpc_js
def win_while(event:str):
    """
    Event loop function for the GUI window. 
    It updates the GUI window elements based on the user interactions with the various components.
    
    Parameters:
    - event (str): The name of the GUI component that was interacted with.
    """
    event,values,window = window_mgr.get_event(),window_mgr.get_values(),window_mgr.get_last_window_method()
    if event == "-NETWORK_NAME-":
        window_mgr.update_values(window=window, key="-NETWORK_NAME_CHECK-", args={"value":True})
        rpc_add_global_bridge["check_list"][event] = ''
        for each in list(get_js().values()):
            if each != event:
                rpc_add_global_bridge["check_list"][each] = ''
                window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)]})
                window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
            # Reset filters
        if each != event:
            rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
            filter_rpc_list_by_selections()
            window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)], "value":''})
            window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
    if event == 'reset':
        # Clear the check list
        for each in list(get_js().values()):
            rpc_add_global_bridge["check_list"][each] = ''
            window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)]})
            if each !="-NETWORK_NAME-":
                window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
        # Reset filters
        rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
        filter_rpc_list_by_selections()
        window_mgr.update_values(window=window, key=each, args={"values":rpc_add_global_bridge["keyed_lists"][get_key_from_value(each)], "value":''})
        if each !="-NETWORK_NAME-":
            window_mgr.update_values(window=window, key=each[:-1]+'_CHECK-', args={"value":False})
    elif event in list(get_js().values()):
        rpc_add_global_bridge["check_list"][event] =window_mgr.get_values()[event]
        window_mgr.update_values(window=window,key=event[:-1]+'_CHECK-',args={"value":True})
    elif '_CHECK-' in event:
        if values[event] == False:
            window_mgr.update_values(window=window,key=event,args={"value":False})
            rpc_add_global_bridge["check_list"][event[:-len('_CHECK-')]+'-'] = ''
        filter_rpc_list_by_selections()
    filter_rpc_list_by_selections()
def filter_rpc_list_by_selections()->list:
    """
    Filters the RPC list based on the user's selections in the GUI window.
    
    Returns:
    - list: A filtered list of RPCs.
    """
    # Start with the full list of RPCs
    rpc_add_global_bridge["recursed_rpc_js_list"] = rpc_add_global_bridge["get_rpc_list"]
    event,values = window_mgr.get_event(),window_mgr.get_values()
    desired_values={}
    for key, value in values.items():
        if '_CHECK-' in str(key):
            if values[key]:
                key = key[:-len('_CHECK-')]+'-'
                desired_values[get_key_from_value(key)]=values[key]
    
    recursive_filtered_list = recursive_json_list(json_list=rpc_add_global_bridge["recursed_rpc_js_list"],desired_values=desired_values)
    event,values = window_mgr.get_event(),window_mgr.get_values()
    filtered_json_list = filter_json_list_values(json_list=recursive_filtered_list,keys=get_keys())
    for key,unique_values in filtered_json_list.items():
        if get_js()[key] in rpc_add_global_bridge["check_list"][get_js()[key]]:
                value = rpc_add_global_bridge["check_list"][get_js()[key]]
        elif  key == 'Network_Name':
            value = rpc_add_global_bridge["check_list"][get_js()[key]]
            unique_values = rpc_add_global_bridge["Network_Names"]
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
    return {"Network_Name":"-NETWORK_NAME-",'Network':"-NETWORK-",'Symbol':"-SYMBOL-",'ChainID':"-CHAIN_ID-",'RPC':"-RPC-",'Block_Explorer':"-BLOCK_EXPLORER-"}
def get_rpc_keys():
    return ['Network_Name', 'ChainID', 'RPC', 'Symbol', 'Block_Explorer','Network']

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
def get_default_rpc_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "rpc_list.json")
    return load_from_file(file_path)
def get_rpc_list(file_path:str=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "rpc_list.json"))->(list or dict):
    """
    Reads and returns the RPC list from a JSON file.
    
    Returns:
    - list: The RPC list.
    """
    if file_path == None:
        return get_default_rpc_list()
    else:
        if os.path.isfile(file_path):
            return load_from_file(file_path)
    return get_default_rpc_list()
def save_rpc_list(json_data:list,file_path:str=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "rpc_list.json"))->(list or dict):
    """
    Reads and returns the RPC list from a JSON file.
    
    Returns:
    - list: The RPC list.
    """
    return dump_to_file(file_path=file_path,json_data=json_data)
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
    elif os.path.isfile(RPC_list):
        RPC_list = get_rpc_list(file_path)
    rpc_add_global_bridge["get_rpc_list"]=[]
    for each in RPC_list:
        rpc_add_global_bridge["get_rpc_list"].append(RPCData(each).return_rpc_js())
    save_rpc_list(json_data = rpc_add_global_bridge["get_rpc_list"])
    rpc_add_global_bridge["total_bool_list"] = []
    rpc_add_global_bridge["recursed_rpc_js_list"]=rpc_add_global_bridge["get_rpc_list"] 
    rpc_add_global_bridge["check_list"]={}
    for each in list(get_js().values()):
        rpc_add_global_bridge["check_list"][each] = ''
    keyed_rpc_lists()
    rpc_add_global_bridge["Network_Names"]=rpc_add_global_bridge["keyed_lists"]["Network_Name"]
    layout = []
    for key,value in get_js().items():
        layout.append([
            get_gui_fun("Text",args={"text":key.replace('_',' ')}),
            get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"][key],"default_text":rpc_add_global_bridge["keyed_lists"][key][0],"key":f"{value}","enable_events":True}),
            get_gui_fun("Checkbox",args={"text":"","default":(key=="Network_Name"),"key":f"{value[:-1]}_CHECK-","enable_events":True}),
            get_push()])
    layout = [[get_menu()],layout,[create_row_of_buttons("OK","Show","reset","Exit"),]]
    window = window_mgr.get_new_window(args={"title":'ADD RPC',"layout":layout,"exit_events":["OK","Exit"],"event_function":"win_while","suppress_raise_key_errors":False, "suppress_error_popups":False, "suppress_key_guessing":False,"finalize":True})
    values = window_mgr.while_basic(window=window)
    rpc={}
    if values:
        for each in values.keys():
            key = get_key_from_value(each)
            if key in get_keys():
                rpc[key] = values[each]
    return RPCData(rpc).return_rpc_js()
## EXAMPLE USAGE
# gui for recursive rpc parameter selection
## rpc_data = Choose_RPC_Parameters_GUI()
# class function for conventionalizing and storing variables
## rpc_manager = RPCData(rpc_data)
#call the Provider via Environment Variable
## w3 = rpc_manager.w3
