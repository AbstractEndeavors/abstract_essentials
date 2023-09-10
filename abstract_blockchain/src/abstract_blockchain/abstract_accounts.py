from .abstract_rpcs import RPCData
from abstract_security.envy_it import get_env_value
class AccountManager:
    def __init__(self, address, rpc):
        self.rpc_manager = RPCData(rpc)
        self.web3 = self.rpc_manager.w3
        self.account_address = self.web3.to_checksum_address(address)
        self.nonce = self.get_transaction_count()
    def check_priv_key(self,priv_key):
        obj = get_env_value(key=private_key)
        if obj:
            return obj
        return priv_key
    def get_transaction_count(self):
        return self.web3.eth.get_transaction_count(self.account_address)
    def sign_transaction(self, txn, private_key):
        return self.web3.eth.account.sign_transaction(txn, self.check_priv_key(private_key))
    def send_transaction(self, to_address, txn_value, private_key):
        gas = self.estimate_gas(to_address,  self.account_address, txn_value)
        txn_info = {
            'to': to_address,
            'from': self.account_address,
            'value': txn_value,
            'gasPrice': 25000000000,
            'gas': gas,
            'nonce': self.nonce,
            'chainId': int(self.rpc_manager.chain_id)
        }
        signed_txn = self.sign_transaction(txn_info, self.check_priv_key(private_key))
        return self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    def estimate_gas(self, to_address, from_address, txn_value):
        return self.web3.eth.estimate_gas({"to": to_address,"from": from_address,"value": txn_value})
