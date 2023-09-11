from abstract_webtools import DynamicRateLimiterManagerSingleton,get_limited_request
from .abstract_rpcs import Choose_RPC_Parameters_GUI,RPCBridge
from .abstract_api_gui import choose_api_gui
from abstract_utilities.type_utils import if_default_return_obj
from abstract_security.envy_it import get_env_value
import json
request_manager = DynamicRateLimiterManagerSingleton.get_instance()
class APIBridge:
    def __init__(self,api_data:str=None,rpc:dict=None,address:str=None):
        if rpc == None:
            rpc = Choose_RPC_Parameters_GUI()
        self.rpc_manager = RPCBridge(rpc)
        self.address = address
        self.address=self.try_check_sum(address=self.address)
        if api_data == None:
            self.api_data = choose_api_gui()
        self.api_data = self.get_api_data_string(api_data_type=api_data,address=self.address)
        self.api_url = f"https://{('api.' if 'api' != self.rpc_manager.scanner[:len('api')] else '')}{self.rpc_manager.scanner}/api?{self.api_data}&apikey={self.api_keys()}"
        self.api_url = self.try_api_url(request_url=self.api_url,self_api_request=True)
        self.response = self.get_response()
    def get_api_data_string(self,api_data_type:str=None,address:str=None):
        address = self.try_check_sum(address)
        if api_data_type == None:
            return api_data_type
        if 'abi' in api_data_type.lower():
            return f"module=contract&action=getabi&address={str(address)}"
        if 'source' in api_data_type.lower() or "code" in api_data_type.lower():
            return f"module=contract&action=getabi&address={str(address)}"
        return api_data_type
    def api_keys(self):
        if self.rpc_manager.scanner in ['ftmscan.com','moonbeam.moonscan.io','polygonscan.com','bscscan.com']:
            return get_env_value(key=self.rpc_manager.scanner)
        return get_env_value(key='etherscan.io')        
    def get_http_variants(self,url:str):
        http_parts = url.split("://")
        http = http_parts[0]
        url_part = http_parts[-1]
        if http[-1]=="s":
            http_2 = http[:-1]
        else:
            http_2 = http+"s"
        return [url,http_2+"://"+url_part]
    def get_api_variants(self,urls:(list or str)):
        if isinstance(urls,str):
            urls= [urls]
        for i,url in enumerate(urls):
            http_parts = url.split("://")
            http = http_parts[0]
            url_part = http_parts[-1][len("api"):]
            if url_part[0]=="-":
                url_part_2 = '.'+url_part[1:]
            elif url_part[0]==".":
                url_part_2 = '-'+url_part[1:]
            urls[i]=http+"://api"+url_part_2
        return urls
    def try_api_url(self,request_url:str=None,self_api_request:bool=False):
        request_url=if_default_return_obj(obj=self.api_url,default=request_url)
        request = self.get_try(request_url=request_url)
        
        if request == None:
            http_variants = []   # Combine the two lists
            http_variants_1 = self.get_http_variants(url=request_url)
            http_variants.append(http_variants_1[0])
            http_variants.append(http_variants_1[0])
            http_variants.append(http_variants_1[1])
            http_variants.append(http_variants_1[1])
            http_variants_2 = self.get_api_variants(urls=http_variants_1)
            http_variants[1]=http_variants_2[0]
            http_variants[3]=http_variants_2[1]
            for request_url in http_variants[1:]:
                request = self.get_try(request_url=request_url)
                if request != None:
                    break  # Break out of loop once we've found a valid request
        if self_api_request:
            self.request = request
        return request_url
    def get_try(self,request_url:str=None,service_name:str=None,low_limit:int=1,high_limit:int=5,limit_epoch:int=1,starting_tokens:int=5,epoch_cycle_adjustment:int=5):
        request_url=if_default_return_obj(obj=self.api_url,default=request_url)
        service_name=if_default_return_obj(obj=self.rpc_manager.scanner,default=service_name)
        try:
            request = self.get_request(request_url=request_url,service_name=service_name,low_limit=low_limit,high_limit=high_limit,limit_epoch=limit_epoch,starting_tokens=starting_tokens)
        except:
            request = None
        return request
    def get_request(self,request_url:str=None, service_name: str = None, low_limit: int = 20, high_limit: int = 30,limit_epoch: int = 60, starting_tokens: int = None,epoch_cycle_adjustment:int=None):
        """
        Make a limited request to the ABI URL using rate-limiting.

        :param request_type: Type of the request (default is None).
        :param request_min: Minimum requests allowed in a rate-limited epoch (default is 10).
        :param request_max: Maximum requests allowed in a rate-limited epoch (default is 30).
        :param limit_epoch: Length of the rate-limited epoch in seconds (default is 60).
        :param request_start: Start of the rate-limited epoch (default is None).
        :param json_data: JSON data for the request (default is None).
        :return: Limited response from the ABI URL.
        """
        request_url=if_default_return_obj(obj=self.api_url,default=request_url)
        request_manager.add_service(service_name=service_name, low_limit=low_limit, high_limit=high_limit, limit_epoch=limit_epoch, starting_tokens=starting_tokens)
        return get_limited_request(request_url=request_url, service_name=service_name)
    def get_response(self,request=None):
        """
        Parse the JSON response and return the ABI.

        :return: Parsed ABI response.
        """
        request=if_default_return_obj(obj=self.request,default=request)
        if request is None:
            return request
        if "result" in request:
            return self.safe_json_loads(request["result"])
        return self.safe_json_loads(request)
    def check_sum(self, address: str=None):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        address = if_default_return_obj(obj=self.address,default=address)
        return self.rpc_manager.w3.to_checksum_address(address)
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        address = if_default_return_obj(obj=self.address,default=address)
        try:
            address = self.check_sum(address)
            return address
        except:
            #raise ValueError("Invalid Ethereum Address")
            pass
    def safe_json_loads(self, json_obj:dict=None):
        """
        Safely load JSON data as a dictionary or a list.

        :param abi: JSON data to load.
        :return: Parsed JSON data as a dictionary or a list.
        :raises TypeError: If the JSON data is of an invalid type.
        """
        json_obj = if_default_return_obj(obj=self.request,default=json_obj)
        try:
            if isinstance(json_obj, (dict, list)):
                return json_obj
            elif isinstance(json_obj, str):
                return json.loads(json_obj)
            else:
                return json.loads(str(json_obj))
        except:
            print("Invalid type for ABI. Must be either str, dict, or list.")
            return json_obj

 
