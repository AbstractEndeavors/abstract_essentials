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
from .abstract_rpcs import RPCData, Choose_RPC_Parameters_GUI
from abstract_webtools import DynamicRateLimiterManagerSingleton, get_limited_request
from abstract_security.envy_it import get_env_value
import json
# Instantiate the rate limiting manager
request_manager = DynamicRateLimiterManagerSingleton.get_instance()
class ABIBridge:
    """
    ABIBridge class provides functionality to interact with Ethereum smart contract ABIs and functions.
    """
    def __init__(self,contract_address:str,rpc:dict=None):
        """
        Initializes the ABIBridge instance.

        :param contract_address: Ethereum contract address.
        :param rpc: RPC configuration dictionary (default is None).
        """
        if rpc == None:
            rpc = Choose_RPC_Parameters_GUI()
        self.rpc = RPCData(rpc)
        self.contract_address = self.try_check_sum(contract_address)
        self.abi_url =f"https://{('api.' if 'api' != self.rpc.scanner[:len('api')] else '')}{self.rpc.scanner}/api?module=contract&action=getabi&address={self.contract_address}&apikey={self.api_keys()}"
        self.request = self.safe_json_loads(self.get_request())
        self.abi = self.get_response()
        self.contract_bridge = self.create_abi_bridge()
        self.contract_functions = self.list_contract_functions()
    def get_request(self, request_type: str = None, request_min: int = 10, request_max: int = 30,
                    limit_epoch: int = 60, request_start: int = None, json_data: dict = None):
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
        request_manager.add_service(request_type, request_min, request_max, limit_epoch, request_start)
        try:
            request = get_limited_request(request_url=self.abi_url, service_name=request_type)
            return request
        except:
            self.abi_url= self.abi_url.replace("api.","api-")
            request = get_limited_request(request_url=self.abi_url, service_name=request_type)
            return request
    def api_keys(self):
        if self.rpc.scanner in ['ftmscan.com','moonbeam.moonscan.io','polygonscan.com','bscscan.com']:
            return get_env_value(key=self.rpc.scanner)
        return get_env_value(key='etherscan.io')
    def get_response(self):
        """
        Parse the JSON response and return the ABI.

        :return: Parsed ABI response.
        """
        return self.safe_json_loads(self.request["result"])

    def try_check_sum(self, address: str):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        try:
            address = self.check_sum(address)
            return address
        except:
            raise ValueError("Invalid Ethereum Address")

    def safe_json_loads(self, abi):
        """
        Safely load JSON data as a dictionary or a list.

        :param abi: JSON data to load.
        :return: Parsed JSON data as a dictionary or a list.
        :raises TypeError: If the JSON data is of an invalid type.
        """
        if isinstance(abi, str):
            return json.loads(abi)
        elif isinstance(abi, (dict, list)):
            return abi
        else:
            raise TypeError("Invalid type for ABI. Must be either str, dict, or list.")

    def check_sum(self, address: str):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        return self.rpc.w3.to_checksum_address(address)

    def create_abi_bridge(self):
        """
        Create a contract bridge using the ABI and contract address.

        :return: Contract bridge instance.
        """
        return self.rpc.w3.eth.contract(address=self.contract_address, abi=self.abi)

    def list_contract_functions(self):
        """
        List all contract functions and their details.

        :return: List of contract function details.
        """
        functions = []
        for item in self.abi:
            if item['type'] == 'function':
                function_details = {
                    "name": item['name'],
                    "inputs": [(i['name'], i['type']) for i in item['inputs']],
                    "outputs": [(o['name'], o['type']) for o in item['outputs']]
                }
                functions.append(function_details)
        return functions

    def get_read_only_functions(self, abi: list = None):
        """
        Get a list of read-only functions from the ABI.

        :param abi: ABI to analyze (default is None, uses instance ABI).
        :return: List of read-only function names.
        """
        if abi is None:
            abi = self.abi
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
        if abi is None:
            abi = self.abi
        for item in self.abi:
            if item['type'] == 'function' and item["name"] == function_name:
                return item["inputs"]
    def call_function(self, function_name, *args, **kwargs):
        """
        Calls a read-only function on the contract.

        :param function_name: Name of the function to call.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: Result of the function call.
        """
        contract_function = getattr(self.contract_bridge.functions, function_name)
        
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
    def create_functions(self, subsinstance, function_name, *args, **kwargs):
        # Access the subsinstance (like "functions" in the contract)
        sub_instance = getattr(self.contract_bridge, subsinstance)  # use self.contract_bridge
            
        # Get the desired function from the subsinstance
        function = getattr(sub_instance, function_name)

        # If there's only one positional argument and no keyword arguments, use it directly.
        # Otherwise, use kwargs as named arguments.
        if len(args) == 1 and not kwargs:
            return function(args[0])
        else:
            return function(**kwargs)
def default_rpc():
    """
    Returns a default RPC configuration dictionary.

    :return: Default RPC configuration dictionary.
    """
    return {'Network': 'Mainnet', 'RPC': 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'Block_Explorer': 'https://etherscan.io', 'ChainID': '0x1', 'Symbol': 'ETH', 'Network_Name': 'Ethereum'}
