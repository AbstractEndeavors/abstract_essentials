"""
abstract_abis.py - ABIBridge Module

This module defines the `ABIBridge` class, which provides functionality for interacting with Ethereum smart contracts' ABIs (Application Binary Interfaces).
It allows you to retrieve and use contract ABIs, call contract functions, and manage rate limiting for API requests.

Classes:
    ABIBridge: A class to interact with Ethereum smart contract ABIs and functions.

Functions:
    default_rpc: Returns a default RPC configuration dictionary.

Example Usage:
    # Create an instance of ABIBridge
    abi_manager = ABIBridge(contract_address='0x3dCCeAE634f371E779c894A1cEa43a09C23af8d5', rpc=default_rpc())
    
    # Retrieve read-only functions from the contract
    read_only_functions = abi_manager.get_read_only_functions()
    
    # Iterate through each read-only function
    for function_name in read_only_functions:
        inputs = abi_manager.get_required_inputs(function_name)
        if len(inputs) == 0:
            result = abi_manager.call_function(function_name)
            print(function_name, result)
        else:
            print(function_name, inputs)
"""
# Import necessary modules and classes
from .abstract_rpcs import RPCBridge, Choose_RPC_Parameters_GUI
from .abstract_apis import APIBridge
from abstract_webtools import DynamicRateLimiterManagerSingleton, get_limited_request
from abstract_utilities.type_utils import if_default_return_obj
from abstract_security.envy_it import get_env_value
import json
# Instantiate the rate limiting manager
request_manager = DynamicRateLimiterManagerSingleton.get_instance()

class ABIBridge:
    """
    ABIBridge class provides functionality to interact with Ethereum smart contract ABIs and functions.
    """
    def __init__(self,contract_address:str=None,rpc:dict=None):
        """
        Initializes the ABIBridge instance.

        :param contract_address: Ethereum contract address.
        :param rpc: RPC configuration dictionary (default is None).
        """
        if not hasattr(self, 'track'):
            self.track = {"address":None,"abi":False}
        if rpc == None:
            rpc = Choose_RPC_Parameters_GUI()
        self.rpc_manager = RPCBridge(rpc_js=rpc)
        self.contract_address=contract_address
        self.contract_address = self.try_check_sum(address=self.contract_address)
        if self.contract_address == None:
            return 
        self.api_manager = APIBridge(api_data="abi",rpc=self.rpc_manager.rpc_js,address=self.contract_address)
        if self.track["address"] == None:
            self.abi_url = self.api_manager.api_url
            self.request = self.api_manager.request
            if not isinstance(self.request,dict):
                self.abi = None
                return self.abi
            else:
                if self.request['status']=='0' or self.request['message']=='NOTOK':
                    self.abi = None
                    return self.abi
            self.abi = self.api_manager.response
        self.contract_bridge = self.create_abi_bridge()
        self.contract_functions = self.list_contract_functions()
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        address = if_default_return_obj(obj=self.contract_address,default=address)
        try:
            address = self.check_sum(address)
            return address
        except:
            #raise ValueError("Invalid Ethereum Address")
            pass
    def check_sum(self, address: str=None):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        address = if_default_return_obj(obj=self.contract_address,default=address)
        return self.rpc_manager.w3.to_checksum_address(address)

    def create_abi_bridge(self,contract_address:str=None,abi:list=None):
        """
        Create a contract bridge using the ABI and contract address.

        :return: Contract bridge instance.
        """
        contract_address =if_default_return_obj(obj=self.contract_address,default=contract_address)
        abi = if_default_return_obj(obj=self.abi,default=abi)
        try:
            abi_bridge = self.rpc_manager.w3.eth.contract(address=contract_address, abi=abi)
        except:
            abi_bridge = None
        return abi_bridge
    def list_contract_functions(self,abi:list=None):
        """
        List all contract functions and their details.

        :return: List of contract function details.
        """
        abi = if_default_return_obj(obj=self.abi,default=abi)
        functions = []
        if abi != None:
            for item in abi:
                if item['type'] == 'function':
                    function_details = {
                        "name": item['name'],
                        "inputs": [(i['name'], i['type']) for i in item['inputs']],
                        "outputs": [(o['name'], o['type']) for o in item['outputs']]
                    }
                    functions.append(function_details)
        return functions

    def get_read_only_functions(self, abi:list=None):
        """
        Get a list of read-only functions from the ABI.

        :param abi: ABI to analyze (default is None, uses instance ABI).
        :return: List of read-only function names.
        """
        abi = if_default_return_obj(obj=self.abi,default=abi)
        read_only_functions = []
        for item in abi:
            if item['type'] == 'function' and (item['stateMutability'] == 'view' or item['stateMutability'] == 'pure'):
                read_only_functions.append(item['name'])
        return read_only_functions

    def get_required_inputs(self, function_name: str, abi: list = None):
        """
        Get the required inputs for a specific function from the ABI.

        :param function_name: Name of the function.
        :param abi: ABI to analyze (default is None, uses instance ABI).
        :return: List of required inputs for the function.
        """
        abi = if_default_return_obj(obj=self.abi,default=abi)
        for item in abi:
            if item['type'] == 'function' and item["name"] == function_name:
                return item["inputs"]
    def call_function(self,*args,function_name:str,contract_bridge=None,**kwargs):
        """
        Calls a read-only function on the contract.

        :param function_name: Name of the function to call.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: Result of the function call.
        """
        
        contract_bridge = if_default_return_obj(obj=self.contract_bridge,default=contract_bridge)
        contract_function = getattr(contract_bridge.functions, function_name)
        # If there are positional arguments (regardless of how many), use them.
        if len(args) == 1 and not kwargs:
            return contract_function(args[0]).call()
        elif args and not kwargs:
            return contract_function(*args).call()
        # If there are keyword arguments, use them.
        elif kwargs:
            return contract_function(**kwargs).call()
        # If no arguments, just call the function.
        else:
            return contract_function().call()
    def create_functions(self,*args,function_name:str,subsinstance:str="functions",contract_bridge=None, **kwargs):
        contract_bridge = if_default_return_obj(obj=self.contract_bridge,default=contract_bridge)
        # Access the subsinstance (like "functions" in the contract)
        sub_instance = getattr(contract_bridge, subsinstance)  # use self.contract_bridge
            
        # Get the desired function from the subsinstance
        contract_function = getattr(sub_instance, function_name)

        # If there's only one positional argument and no keyword arguments, use it directly.
        # Otherwise, use kwargs as named arguments.
        if len(args) == 1 and not kwargs:
            return contract_function(args[0])
        elif args and not kwargs:
            return contract_function(*args)
        # If there are keyword arguments, use them.
        elif kwargs:
            return contract_function(**kwargs)
        # If no arguments, just call the function.
        else:
            return contract_function()

