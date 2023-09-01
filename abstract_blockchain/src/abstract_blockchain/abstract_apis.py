from web3 import Web3
from web3.auto import w3
from abstract_webtools import SafeRequest
from abstract_security.envy_it import get_env_value
from abstract_utilities.time_utils import get_sleep,get_time_stamp
from abstract_utilities.json_utils import create_and_read_json,dump_to_file
from abstract_webtools import SafeRequest,strip_web
from web3._utils.events import get_event_data
from abstract_rpcs import Choose_RPC_Parameters_GUI,categorize_rpc_items,get_rpc_list
safe_requester = SafeRequest()
def changeGlob(var,val):
    globals()[var]=val
def make_request_json(request_type:str=None,file_path:str="request_timer.json",last_request_time:(int or float)=None,request_wait_limit:(int or float)=1.5,json_data:dict=None):
    if json_data == None:
        json_data = {}
        if last_request_time == None:
            last_request_time = get_time_stamp() - request_wait_limit
        json_default ={"last_request":last_request_time,"wait_limit":request_wait_limit}
    if request_type!=None:
        json_data[request_type]= json_default
    else:
        json_data = json_default
    return json_data  
def get_request_time(request_type:str=None,file_path:str="request_timer.json",last_request_time:(int or float)=None,request_wait_limit:(int or float)=1.5,json_data:dict=None)->(int or float):
    json_data = make_request_json(request_type=request_type,file_path=file_path,request_wait_limit=request_wait_limit,json_data=json_data)
    json_response = create_and_read_json(file_path,json_data=json_data)
    return json_response
def save_request_time(request_type:str=None,file_path:str="request_timer.json",last_request_time:(int or float)=get_time_stamp(),request_wait_limit:(int or float)=1.5,json_data:dict=None)->(int or float):
    json_data = make_request_json(request_type=request_type,file_path=file_path,request_wait_limit=request_wait_limit,json_data=json_data)
    dump_to_file(file_path=file_path, json_data=json_data)
def get_request(url,request_type:str=None,file_path:str="request_timer.json",request_wait_limit:(int or float)=1.5,json_data:dict=None):
    request_data = get_request_time(request_type=request_type,file_path=file_path,request_wait_limit=request_wait_limit,json_data=json_data)
    source_code = safe_requester.make_request(url=url,last_request_time=request_data["last_request"],request_wait_limit=request_data["wait_limit"])
    save_request_time(request_type=request_type,file_path=file_path,last_request_time=request_data["last_request"],request_wait_limit=request_data["wait_limit"])
    return source_code
def apiKeys(scanner):
    if scanner in ['ftmscan.com','moonbeam.moonscan.io','polygonscan.com','bscscan.com']:
        return get_env_value(key=scanner)
    return get_env_value(key='etherscan.io')
def chooseIt():
    global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3
    netName,chainId,rpc,nativeCurrency,explorer,scanner = fun.eatAllLs([netName,chainId,rpc,nativeCurrency,explorer,scanner],[' ',''])
def getAbi(add,scanner):
    return get_request('https://api.'+str(scanner)+'/api?module=contract&action=getabi&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
def getSource(add,scanner):
    return get_request('https://api.'+str(scanner)+'/api?module=contract&action=getsourcecode&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
def getData(s,dot,typ,add,scanner):
    try:
        result = shortsites('http'+str(s)+'://api'+str(dot)+str(scanner)+'/api?module=contract&action='+typ+'&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
        return 'http'+str(s)+'://api'+str(dot)+str(scanner),result
    except:
      return False
def getRPC(js):
    if 'RPC' in js:
        return js['RPC']
    return False
def checkSum(x):
    return w3.to_checksum_address(x)
def tryCheckSum(x):
    try:
        y = w3.to_checksum_address(x)
        return y
    except:
        return False
def extractRPCdata(js):
    js = categorize_rpc_items(js)
    changeGlob('Symbol',js['Symbol'])
    changeGlob('Network_Name',js['Network_Name'])
    changeGlob('Block_Explorer',js['Block_Explorer'])
    changeGlob('RPC',js['RPC'])
    changeGlob('ChainID',js['ChainID'])
    changeGlob('scanner',strip_web(js['Block_Explorer']))
    changeGlob("w3",Web3(Web3.HTTPProvider(js["RPC"])))
    return Symbol,Network_Name,RPC,ChainID,Block_Explorer,scanner,Web3(Web3.HTTPProvider(js['RPC']))  
