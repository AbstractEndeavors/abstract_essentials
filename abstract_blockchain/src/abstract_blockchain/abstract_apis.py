from web3 import Web3
from abstract_security.envy_it import get_env_value
from abstract_webtools import DynamicRateLimiterManagerSingleton,get_limited_request
from web3._utils.events import get_event_data
from .abstract_rpcs import Choose_RPC_Parameters_GUI,RPCData
from .abstract_api_gui import choose_api_gui
request_manager = DynamicRateLimiterManagerSingleton.get_instance()
def changeGlob(var,val):
    globals()[var]=val
def get_request(url,request_type:str=None,request_min:int=10,request_max:int=30,limit_epoch:int=60,request_start:int=None,json_data:dict=None):
    request_manager.add_service(request_type,request_min, request_max, limit_epoch,request_start)
    return get_limited_request(request_url=url,service_name=request_type)
def apiKeys(scanner):
    if scanner in ['ftmscan.com','moonbeam.moonscan.io','polygonscan.com','bscscan.com']:
        return get_env_value(key=scanner)
    return get_env_value(key='etherscan.io')
def getAbi(add,scanner):
    return get_request(url=f"https://api.{scanner}/api?module=contract&action=getabi&address={checkSum(str(add))}&apikey={str(apiKeys(scanner))}")
def getSource(add,scanner):
    return get_request(url=f"https://api.{str(scanner)}/api?module=contract&action=getsourcecode&address={checkSum(str(add))}&apikey={str(apiKeys(scanner))})")
def getData(s,dot,typ,add,scanner):
    try:
        result = get_request(url='http'+str(s)+'://api'+str(dot)+str(scanner)+'/api?module=contract&action='+typ+'&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
        return 'http'+str(s)+'://api'+str(dot)+str(scanner),result
    except:
      return False
def checkSum(address:str):
    return w3.to_checksum_address(address)
def tryCheckSum(address:str):
    try:
        address = checkSum(address)
        return address
    except:
        return False
def extractRPCdata(js):
    rpc_data = RPCData(js)
    changeGlob('Symbol',rpc_data.symbol)
    changeGlob('Network_Name',rpc_data.network_name)
    changeGlob('Block_Explorer',rpc_data.block_explorer)
    changeGlob('RPC',rpc_data.rpc)
    changeGlob('ChainID',rpc_data.chain_id)
    changeGlob('scanner',rpc_data.scanner)
    changeGlob("w3",rpc_data.w3)
    return Symbol,Network_Name,RPC,ChainID,Block_Explorer,scanner,w3
def get_api_gui():
    rpc = extractRPCdata(Choose_RPC_Parameters_GUI())
    url = f"https://api.{str(scanner)}/api?{choose_api_gui()}{str(apiKeys(scanner))}"
    response = get_request(url=url)
    return response

