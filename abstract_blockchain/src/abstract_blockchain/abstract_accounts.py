from .abstract_rpcs import RPCBridge
from .abstract_apis import APIBridge
from eth_account import Account
from abstract_utilities.type_utils import if_default_return_obj,is_number
from abstract_security.envy_it import get_env_value
class ACCTBridge:
    def __init__(self, env_key:str=None,address:str=None, rpc:dict=None):
        self.rpc_manager = RPCBridge(if_default_return_obj(obj=rpc,default=RPCBridge().get_default_rpc()))
        self.web3 = self.rpc_manager.w3
        self.private_key = self.check_priv_key(if_default_return_obj(obj=env_key,default=env_key))
        self.account_address = if_default_return_obj(obj=self.get_address_from_private_key(self.private_key),default=address)
        self.account_address = self.try_check_sum(address=self.account_address)
        self.nonce = self.get_transaction_count()
    def check_priv_key(self,private_key):
        obj = get_env_value(key=private_key)
        if obj:
            return obj
        return private_key
    def get_address_from_private_key(self,private_key: str) -> str:
        account = Account.from_key(private_key)
        return self.try_check_sum(account.address)
    def build_txn(self, contract_bridge,from_address:str=None,to_address:str=None,txn_value:int=None,gasPrice:int=None,gas:int=None):
        return contract_bridge.build_transaction(self.get_txn_info(from_address=from_address,to_address=to_address,txn_value=txn_value,gasPrice=gasPrice,gas=gas))
    def get_txn_info(self, to_address:str=None,from_address:str=None,txn_value:int=None,gasPrice:int=None,gas:int=None):
        from_address = str(self.try_check_sum(if_default_return_obj(obj=self.account_address,default=from_address)))
        if not is_number(gasPrice):
            if isinstance(gasPrice,str):
                gasPrice = self.estimate_gas(gas_strategy=gasPrice)
        gas_price = if_default_return_obj(obj=self.estimate_gas(),default=gasPrice)
        if not is_number(gas):
            if isinstance(gas,str):
                gas = self.estimate_gas(gas_strategy=gasPrice)
        gas = if_default_return_obj(obj=self.estimate_gas(gas_strategy="suggestBaseFee"),default=gas)
        txn_info = {
            'from': from_address,
            'gasPrice':gas_price,
            'gas': gas,
            'nonce': self.nonce,
            'chainId': self.rpc_manager.chain_id,
            'nonce':self.nonce}
        if txn_value != None:
            txn_info["value"]=txn_value
        if to_address != None:
            txn_info["to"] = str(self.try_check_sum(to_address))
        return txn_info
    def check_sum(self, address:str=None):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        #address = if_default_return_obj(obj=self.get_address_from_private_key(self.private_key),default=address)
        return self.rpc_manager.w3.to_checksum_address(address)
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        #address = if_default_return_obj(obj=self.get_address_from_private_key(self.private_key),default=address)
        try:
            address = self.check_sum(address)
            return address
        except:
            raise ValueError("Invalid Ethereum Address")
    def get_transaction_count(self):
        return self.web3.eth.get_transaction_count(self.account_address)
    def sign_transaction(self, tx_info, private_key:str=None):
        return self.web3.eth.account.sign_transaction(tx_info, self.check_priv_key(if_default_return_obj(obj=self.private_key,default=private_key)))
    def send_transaction(self, tx_info, private_key:str=None):
        signed_txn = self.sign_transaction(tx_info=tx_info, private_key=self.check_priv_key(if_default_return_obj(obj=self.private_key,default=private_key)))
        return self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    def estimate_gas(self,gas_strategy:str="safe"):
        api_manager = APIBridge(api_data="module=gastracker&action=gasoracle",rpc=self.rpc_manager.rpc_js)
        for key in api_manager.response.keys():
            if gas_strategy.lower() in key.lower():
                response = api_manager.response[key]
                if key == "suggestBaseFee":
                    return int(float(response)*1000)
                return self.web3.to_wei(int(response), 'gwei')
