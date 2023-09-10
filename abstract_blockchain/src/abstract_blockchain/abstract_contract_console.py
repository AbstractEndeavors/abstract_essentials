from abstract_gui import create_window_manager,agf,get_push
from .abstract_rpcs import rpc_win_while,get_rpc_layout,get_rpc_js,RPCData,get_default_rpc_list
from .abstract_abis import ABIBridge,default_rpc
# Initialize the window manager and bridge 
# (Assuming you still want to name it "blockchain_gui_consol")
new_window_mgr, new_bridge, new_script_name = create_window_manager(script_name="blockchain_gui_consol", global_var=globals())
new_bridge_global = new_bridge.return_global_variables(new_script_name)
def mkBool(x):
    if str(x).lower() in ['true','t','yes','y','0']:
        return str(0)
    return str(1)
def isUintSt(x):
    if x[:len('uint')].lower() == 'uint' and str(x).lower() in ['uint8','uint16','uint32','uint64','uint128','uint256']:
        return True
    return False
def isIntSt(x):
    if x[:len('int')].lower() == 'int' and str(x).lower() in ['int8','int16','int32','int64','int128','int256']:
        return True
    return False
def isAddress(x):
    if x[:len('address')].lower() == 'address':
        return True
def isBool(x):
    if x[:len('bool')].lower() == 'bool':
        return True
def isString(x):
    if x[:len('string')].lower() == 'string':
        return True
def isBytes(x):
    if x[:len('bytes')].lower() == 'bytes':
        return True
def get_type(input_type,value):
    if value == '':
        return str('')
    if isUintSt(input_type) or isIntSt(input_type):
        return int(value)
    elif isBytes(input_type):
        return kek(value)
    elif isAddress(input_type):
        return try_check_sum(str(value))
    elif isBool(input_type):
        return bool(str(value))
    else:
        return str(value)
def default_rpc():
    return {"Network": "Mainnet", "RPC": "https://rpc.ankr.com/eth", "Block_Explorer": "https://etherscan.io", "ChainID": "0x1", "Symbol": "ETH", "Network_Name": "Ethereum"}
def get_w3():
    if "rpc_manager" not in new_bridge_global:
        return RPCData(default_rpc()).w3
    if not isinstance(new_bridge_global["rpc_manager"].w3,type(RPCData(default_rpc()).w3)):
        print("rpc w3 no good")
        return RPCData(default_rpc()).w3
    return new_bridge_global["rpc_manager"].w3
def get_size(input_type):
    if isUintSt(input_type) or isIntSt(input_type):
        return 24
    elif isBytes(input_type):
        return len("0x****************************************************************")+4
    elif isAddress(input_type):
        return len("0x****************************************")+4
    elif isBool(input_type):
        return 4
    else:
        return len("0x****************************************************************")+4
def try_check_sum(address:str):
    try:
        address = get_w3().to_checksum_address(str(address))
        return address
    except:
        return False
def lsNum():
    return str('1,2,3,4,5,6,7,8,9,0').split(',')
def isNum(x):
    if isInt(x):
        return True
    for k in range(0,len(str(x))):
        if str(x)[k] not in lsNum():
            return False
    return True
def isLs(ls):
    if type(ls) is list:
        return True
    return False
def isList(x):
    if x[-1] == ']':
        if x[:-1].split('[')[-1] == '':
            return [x],'*',0
        lsN = []
        for i in range(0,int(x[:-1].split('[')[-1])):
            lsN.append(x)    
        return lsN,i,0
    return x,1,0
def isInt(x):
  if type(x) is int:
    return True
  return False
def call_function(function_name):
    values = new_window_mgr.get_values()
    inputs = {}
    output_key = None
    for key, value in values.items():
        if f"-INPUT_{function_name}_" in key:
            input_name = f"{key.split('_')[-2]}"
            input_type = f"{key.split('_')[-1][:-1]}"# Assuming the name of the input is second to the last in the split result
            inputs[input_name] = get_type(input_type,value)
        elif f"-OUTPUT_{function_name}_" in key:
            output_key = key
    try:
        # If there's only one input and it's of type address
        if len(list(inputs.keys())) == 1:
            result = new_bridge_global["abi_manager"].call_function(function_name, inputs[list(inputs.keys())[0]])
        # For multiple inputs, unpack them as positional arguments
        elif inputs:
            args = tuple(inputs.values())  # Convert the dictionary values to a tuple
            result = new_bridge_global["abi_manager"].call_function(function_name, *args)
        else:
            result = new_bridge_global["abi_manager"].call_function(function_name=function_name)
        if output_key:
            new_window_mgr.update_values(key=output_key, args={"value": result})
    except Exception as e:
        print(f"Error calling function: {e} \nInputs: {inputs}")
def contract_win_while(event: str):
    if event == "-CALL_ALL_READ_ONLY-":
        read_only_list = new_bridge_global["abi_manager"].get_read_only_functions()
        for each in read_only_list:
            call_function(each)
    if "-CALL-" in event:
        # Extracting inputs and outputs associated with the function
        call_function(event.split("-")[2])
def win_while(event: str):
    rpc_win_while(event)
    values = new_window_mgr.get_values()
    rpc_manager = get_rpc()
    if event == "-OK_RPC-":
        new_bridge_global["rpc_manager"]=rpc_manager
        print(rpc_manager.rpc_js)
    if event == "-GET_ABI-":
        contract_address = values["-CONTRACT_ADDRESS-"]
        new_bridge_global["abi_manager"] = ABIBridge(contract_address=contract_address, rpc=rpc_manager.rpc_js)
        function_js = {}
        for each in new_bridge_global["abi_manager"].abi:
            if each["type"] == "function":
                if each["stateMutability"] not in function_js:
                    function_js[each["stateMutability"]] = []
                inputs = _parse_io(each.get("inputs", []),function_name=each["name"])
                outputs = _parse_io(each.get("outputs", []), is_output=True,function_name=each["name"])
                layout = inputs + outputs  # Combine inputs and outputs
                button = [agf("Button", args={"button_text": f"Call {each['name']}", "key": f"-CALL-{each['name']}-"})]
                layout.append(button)
                function_js[each["stateMutability"]].append(
                    agf("Frame", args={"title": each["name"], "layout": layout})
                )
        # Organizing framed groups with 4 columns per row
        all_layouts = [agf("Button", args={"button_text": f"Call All Read Only", "key": "-CALL_ALL_READ_ONLY-"})]
        for state, funcs in function_js.items():
            rows = [funcs[i:i+7] for i in range(0, len(funcs), 7)]
            state_layout = []
            for row in rows:
                state_layout.append(row)
            all_layouts.append([agf("Frame", args={"title": state, "layout": state_layout})])
        new_window = new_window_mgr.get_new_window(title="functions", layout=all_layouts, event_function="contract_win_while")
        new_window_mgr.while_basic(window=new_window)
    
def _parse_io(io_data,function_name:str, is_output=False):
    layout = []
    for i, io_type in enumerate(io_data):
        text = f"{io_type['name']}({io_type['type']}): "
        key_suffix = "OUTPUT" if is_output else "INPUT"
        key = f"-{key_suffix}_{function_name}{'_{i}' if key_suffix is 'INPUT' else ''}_{io_type['name']}_{io_type['type']}-"
        if is_output:
            layout.append([agf("Text", args={"text": text}),get_push(), agf("Input", args={"size": (get_size(io_type['type']), 1), "key": key, "disabled": True})])
        else:
            layout.append([agf("Text", args={"text": text}),get_push(),  agf("Input", args={"size": (get_size(io_type['type']), 1), "key": key})])
    return layout

# If you need the ABI helper function in the new script, define it here 
def get_abi():
    frame_layout = [agf("Input",args={"key":"-CONTRACT_ADDRESS-"}),
                    agf("Button", args={"button_text":"GET ABI","enable_events":True,"key":"-GET_ABI-"})]
    return agf("Frame", "ABI", frame_layout)
def get_rpc():
    rpc={}
    rpc_js = get_rpc_js()
    for rpc_key,window_key in rpc_js.items():
        rpc[rpc_key] = new_window_mgr.get_values()[window_key]
    return RPCData(rpc)
def abstract_contract_console_main():
    # Get the rpc_layout and other associated values
    rpc_list = get_default_rpc_list()
    rpc_layout= [[agf("Frame", "RPC_LAY",args={"layout":get_rpc_layout(RPC_list=rpc_list,window_mgr=new_window_mgr)})]]

    # Construct the final layout
    new_layout = [get_abi(),rpc_layout]

    # Create and run the window
    new_window = new_window_mgr.get_new_window(title="New Blockchain Console", layout=[new_layout], event_function="win_while")
    new_window_mgr.while_basic(window=new_window)
