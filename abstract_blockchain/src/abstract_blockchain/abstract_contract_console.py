from abstract_gui import create_window_manager,agf,get_push
from .abstract_rpcs import rpc_win_while,get_rpc_layout,get_rpc_js,RPCBridge
from .abstract_abis import ABIBridge
from .abstract_accounts import ACCTBridge
import codecs
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
def isTuple(x):
    if x[:len('tuple')].lower() == 'tuple':
        return True
def getCodex(obj: str) -> str:
    # Convert a hex string to bytes and then decode to UTF-8
    b = bytes.fromhex(obj)
    return codecs.decode(b, 'UTF-8')
def get_keccak(obj: str) -> str:
    # Create a keccak hash of a string and get its hexadecimal representation
    return get_w3().keccak(text=str(obj)).hex()
def read_hex(hb: bytes) -> str:
    # Convert bytes to hex string
    return hb.hex()
def get_hex_data(obj: str) -> int:
    # Convert a hex string to an integer
    return int(obj, 16)
def can_be_converted_from_keccak(obj: str) -> bool:
    try:
        # Try to get the keccak hash of the object
        keccak_hash = get_keccak(obj)
        # Check if the object can be decoded from hex to UTF-8
        decoded_string = getCodex(keccak_hash)
        return True
    except Exception:
        return False
def string_to_bytes(input_type: str, value: (str or bytes)) -> str:
    # If the type is dynamic "bytes"
    if input_type == "bytes":
        if isinstance(value, str) and not value.startswith("0x"):
            value_bytes = value.encode('utf-8')
        elif isinstance(value, str) and value.startswith("0x"):
            value_bytes = bytes.fromhex(value[2:])
        else:
            value_bytes = value
    else:
        # Determine the target size from the input_type
        size = int(input_type[5:])
        
        # If the value is a regular string, encode it
        if isinstance(value, str) and not value.startswith("0x"):
            value_bytes = value.encode('utf-8')
        # If the value starts with "0x", convert it to bytes
        elif isinstance(value, str) and value.startswith("0x"):
            value_bytes = bytes.fromhex(value[2:])
        # If the value is already bytes, just use it
        else:
            value_bytes = value
        
        # Adjust size of the bytes value
        if len(value_bytes) > size:
            # Truncate if too long
            value_bytes = value_bytes[:size]
        elif len(value_bytes) < size:
            # Pad with zeros if too short
            value_bytes += b'\x00' * (size - len(value_bytes))
        
    # Return as hex string
    return '0x' + value_bytes.hex()
def get_type(input_type, value, output=False):
    if value == '':
        return str('')
    if isUintSt(input_type) or isIntSt(input_type):
        return int(value)
    elif isBytes(input_type):
        if output == True:
            if can_be_converted_from_keccak(value):
                # Try to get the keccak hash of the object
                keccak_hash = get_keccak(obj=value)
                # Check if the object can be decoded from hex to UTF-8
                decoded_string = getCodex(obj=keccak_hash)
                return str(decoded_string)
        return str(string_to_bytes(input_type=input_type,value=value))
    elif isTuple(input_type):
        return tuple(value)
    elif isAddress(input_type):
        return try_check_sum(str(value))
    elif isBool(input_type):
        value = bool(str(value))
        if output == True:
            return {'0':"True","1":"False"}[str(value)]
        return value
    return str(value)
            
def get_w3():
    if "rpc_manager" not in new_bridge_global:
        return RPCBridge().w3
    if not isinstance(new_bridge_global["rpc_manager"],type(RPCBridge())):
        print("rpc w3 no good")
        return RPCBridge().w3
    return new_bridge_global["rpc_manager"].w3
def get_size(input_type):
    if isUintSt(input_type) or isIntSt(input_type) or isString(input_type):
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
    output_keys= []
    for key, value in values.items():
        if f"-INPUT_{function_name}_" in key:
            input_name = f"{key.split('_')[-2]}"
            input_type = f"{key.split('_')[-1][:-1]}"# Assuming the name of the input is second to the last in the split result
            inputs[input_name] = get_type(input_type,value)
        elif f"-OUTPUT_{function_name}_" in key:
            if key not in output_keys:
                output_keys.append(key)
    try:
        # If there's only one input and it's of type address
        #if len(list(inputs.keys())) == 1:
        #    result = new_bridge_global["abi_manager"].call_function(inputs[list(inputs.keys())[0]],function_name=function_name)
        # For multiple inputs, unpack them as positional arguments
        if inputs:
            args = tuple(inputs.values())  # Convert the dictionary values to a tuple
            contract_bridge = new_bridge_global["abi_manager"].create_functions(*args,function_name=function_name,subsinstance="functions")
        else:
            contract_bridge = new_bridge_global["abi_manager"].create_functions(function_name=function_name,subsinstance="functions")
        if get_funciton_mutability(function_name).lower() in ["pure","view"]:
            result = contract_bridge.call()
        else:
            txn_info = new_bridge_global["account_manager"].build_txn(contract_bridge=contract_bridge)
            result = new_bridge_global["account_manager"].send_transaction(tx_info=txn_info)
        if len(output_keys)>0:
            if len(output_keys) == 1:
                new_window_mgr.update_values(key=output_keys[0], args={"value": str(get_type(output_keys[0].split('_')[-1][:-1],result,output=True))})
            if len(output_keys)>1:
                if not isinstance(result,list):
                    if isinstance(result,str):
                        result=result.split(',')
                    if isinstance(result,set):
                        result=list(result)
                    else:   
                        result = [result]
                for each_output_key in output_keys:
                    num = int(each_output_key[len(f"-OUTPUT_{function_name}_"):].split('_')[0])
                    new_window_mgr.update_values(key=each_output_key, args={"value": str(get_type(each_output_key.split('_')[-1][:-1],result[num],output=True))})
    except Exception as e:
        print(f"Error calling function: {e} \nInputs: {inputs}")
def get_funciton_mutability(function_name):
    for each in new_bridge_global["abi_manager"].abi:
        if each["type"] == "function":
            if each["name"] == function_name:
                return each["stateMutability"]
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
        print(new_bridge_global["rpc_manager"].rpc_js)
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
        new_window = new_window_mgr.get_new_window(title=f"{new_window_mgr.get_values(window=new_bridge_global['main_window'])['-NETWORK_NAME-']} contract {contract_address}", layout=all_layouts, event_function="contract_win_while")
        new_window_mgr.while_basic(window=new_window)
    if event == "-DERIVE_RPC-":
        contract_address = values["-CONTRACT_ADDRESS-"]
        new_bridge_global["abi_manager"]=determine_correct_rpc(contract_address=contract_address,rpc_list=new_bridge_global["rpc_list"])
        rpc = new_bridge_global["abi_manager"].rpc_manager.rpc_js
        if isinstance(rpc,dict):
            for key,value in rpc.items():
                new_window_mgr.update_values(key=get_rpc_js()[key],args={"value":value})
    if event == "-ASSOCIATE_ACCOUNT-":
        new_bridge_global["account_manager"] = ACCTBridge(env_key=values["-ACCOUNT_ENV_KEY-"],rpc=get_rpc())
        new_window_mgr.update_values(key="-ACCOUNT_ADDRESS-",args={"value":new_bridge_global["account_manager"].account_address})
def _parse_io(io_data,function_name:str, is_output=False):
    layout = []
    for i, io_type in enumerate(io_data):
        text = f"{io_type['name']}({io_type['type']}): "
        key_suffix = "OUTPUT" if is_output else "INPUT"
        key = f"-{key_suffix}_{function_name}_{i}_{io_type['name']}_{io_type['type']}-"
        component_type="Input"
        size = (get_size(io_type['type']), 1)
        if io_type['type'].lower() in ["bytes","string"]:
            component_type = "Multiline"
            size = (get_size(io_type['type']), 3)
        if is_output:
            layout.append([agf("Text", args={"text": text}),get_push(), agf(component_type, args={"size": size,"key": key, "disabled": True})])
        else:
            layout.append([agf("Text", args={"text": text}),get_push(),  agf(component_type, args={"size": size, "key": key})])
    return layout
def get_account_layout():
    frame_layout = [[agf("Text", args={"text": "ENV Key:"}),get_push(),agf("Input",args={"key":"-ACCOUNT_ENV_KEY-"})],
                    [agf("Text", args={"text": "Account Address"}),get_push(),agf("Input",args={"default_text":"No Address Found","key":"-ACCOUNT_ADDRESS-","disabled":True})],
                    [agf("Button", args={"button_text":"Associate Account","enable_events":True,"key":"-ASSOCIATE_ACCOUNT-"})]]
    return [agf("Frame", "Account", args={"layout":frame_layout})]
# If you need the ABI helper function in the new script, define it here 
def get_abi():
    frame_layout = [agf("Input",args={"key":"-CONTRACT_ADDRESS-"}),
                    agf("Button", args={"button_text":"GET ABI","enable_events":True,"key":"-GET_ABI-"}),
                    agf("Button", args={"button_text":"DERIVE RPC","enable_events":True,"key":"-DERIVE_RPC-"})]
    return agf("Frame", "ABI", frame_layout)
def get_rpc():
    rpc={}
    rpc_js = get_rpc_js()
    for rpc_key,window_key in rpc_js.items():
        rpc[rpc_key] = new_window_mgr.get_values(window=new_bridge_global["main_window"])[window_key]
    return RPCBridge(rpc)
def determine_correct_rpc(contract_address:str,rpc_list:list=None):
    if rpc_list == None:
        if "rpc_list" in new_bridge_global:
            if new_bridge_global["rpc_list"] != None:
                rpc_list = new_bridge_global["rpc_list"]
            else:
                rpc_list = RPCBridge().get_default_rpc_list()
        else:
            rpc_list = RPCBridge().get_default_rpc_list()
    for rpc in rpc_list:
        abi_manager = ABIBridge(contract_address=contract_address,rpc=rpc)
        if isinstance(abi_manager.abi,list):
            break
    return abi_manager
def abstract_contract_console_main(rpc_list:list=None):
    if rpc_list == None:
        rpc_list = RPCBridge().get_default_rpc_list()
    new_bridge_global["rpc_list"]=rpc_list
    # Get the rpc_layout and other associated values
    rpc_layout= [[agf("Frame", "RPC_LAY",args={"layout":get_rpc_layout(rpc_list=new_bridge_global["rpc_list"],window_mgr=new_window_mgr)})]]
    # Construct the final layout
    new_layout = [[get_account_layout()],get_abi(),rpc_layout]
    # Create and run the window
    new_window = new_window_mgr.get_new_window(title="New Blockchain Console", layout=[new_layout], event_function="win_while")
    new_bridge_global["main_window"] = new_window
    new_window_mgr.while_basic(window=new_window)
abstract_contract_console_main()
