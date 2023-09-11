import os
from abstract_utilities.json_utils import load_from_file,dump_to_file
from abstract_utilities.list_utils import filter_json_list_values,recursive_json_list
from abstract_utilities.type_utils import if_default_return_obj
from abstract_gui import create_window_manager,get_gui_fun,create_row_of_buttons,get_menu,get_push,sg
from web3 import Web3
window_mgr,rpc_global_bridge,rpc_add_script_name=create_window_manager(global_var=globals())
rpc_add_global_bridge=rpc_global_bridge.return_global_variables(rpc_add_script_name)
class RPCBridge:
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """
    def __init__(self, rpc_js:dict=None):
        """
        Initializes the RPCBridge instance with RPC parameters.

        :param rpc_js: Dictionary containing RPC parameters.
        """
        self.rpc_js = self.categorize_rpc_items(if_default_return_obj(obj=self.get_default_rpc(),default=rpc_js))
        self.symbol = self.rpc_js['Symbol']
        self.network_name = self.rpc_js['Network_Name']
        self.block_explorer = self.rpc_js['Block_Explorer']
        self.rpc = self.rpc_js['RPC']
        self.chain_id = self.rpc_js['ChainID']
        self.scanner = self.strip_web(self.block_explorer)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))

    def categorize_rpc_items(self,rpc_js:dict=None):
        rpc_js=if_default_return_obj(obj=self.get_default_rpc(),default=rpc_js)
        
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
            stripped_value = RPCBridge.strip_web(value)
            if len(value) != len(stripped_value):
                url_candidates.append(value)  # Keep the original URL
                continue
            # Remaining items go to string items list
            string_items.append(value)
        
        # Classify URLs
        url_candidates = sorted(url_candidates, key=lambda x: (x.startswith('http://rpc') or x.startswith('https://rpc'), 'rpc' in x, -RPCBridge.count_slashes(x)), reverse=True)
        if len(url_candidates)>0:
            categorization["RPC"] = url_candidates[0]
        if len(url_candidates)>1:
            categorization["Block_Explorer"] = url_candidates[1]
        if len(categorization["Block_Explorer"]) > len(categorization["RPC"]):
            rpc=categorization["RPC"]
            categorization["RPC"]=categorization["Block_Explorer"]
            categorization["Block_Explorer"]=rpc
        # Classify ChainID
        string_items = sorted(string_items, key=lambda x: -RPCBridge.percent_integer_of_string(x))
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
    
    def return_rpc_js(self,rpc_js:dict=None):
        return if_default_return_obj(obj=self.rpc_js,default=rpc_js)
    def is_hexadecimal(s):
        # Regular expression to match a valid hexadecimal string
        hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
        return bool(hex_pattern.match(s))
    def get_default_rpc(self, Network_Name:str="Ethereum", rpc_list:list=None):
        rpc_list=if_default_return_obj(obj=self.get_default_rpc_list(),default=rpc_list)
        for rpc in rpc_list:
            if rpc["Network_Name"].lower() == Network_Name.lower():
                return rpc
        return {"Network": "Mainnet", "RPC": "https://rpc.ankr.com/eth", "Block_Explorer": "https://etherscan.io", "ChainID": "0x1", "Symbol": "ETH", "Network_Name": "Ethereum"}
    def get_default_rpc_list(self):
        return [{"Symbol": "Arbitrum", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/arbitrum", "ChainID": "42161", "Block_Explorer": "https://arbiscan.io/", "Network_Name": "Arbitrum"}, {"Symbol": "AVAX", "Network": "Mainnet", "RPC": "https://api.avax.network/ext/bc/C/rpc", "ChainID": "43114", "Block_Explorer": "https://snowtrace.io", "Network_Name": "Avalanche"}, {"Symbol": "AVAX", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/avalanche", "ChainID": "43114", "Block_Explorer": "https://snowtrace.io", "Network_Name": "Avalanche"}, {"Symbol": "AVAX", "Network": "Testnet", "RPC": "https://api.avax-test.network/ext/bc/C/rpc", "ChainID": "43113", "Block_Explorer": "https://testnet.snowtrace.io", "Network_Name": "Avalanche"}, {"Symbol": "AVAX", "Network": "Testnet", "RPC": "https://localhost:9650/ext/bc/C/rpc", "ChainID": "43112", "Block_Explorer": "https://snowtrace.io", "Network_Name": "Avalanche"}, {"Symbol": "BNB", "Network": "Mainnet", "RPC": "https://bsc-dataseed.binance.org", "ChainID": "56", "Block_Explorer": "https://bscscan.com", "Network_Name": "Binance Smart Chain"}, {"Symbol": "BNB", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/bsc", "ChainID": "56", "Block_Explorer": "https://bscscan.com", "Network_Name": "Binance Smart Chain"}, {"Symbol": "BNB", "Network": "Testnet", "RPC": "https://data-seed-prebsc-1-s1.binance.org:8545", "ChainID": "97", "Block_Explorer": "https://testnet.bscscan.com", "Network_Name": "Binance Smart Chain"}, {"Symbol": "CELO", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/celo", "ChainID": "42220", "Block_Explorer": "https://celoscan.com", "Network_Name": "Celo"}, {"Symbol": "CONDOR", "Network": "Testnet", "ChainID": "188881", "Network_Name": "Condor"}, {"Symbol": "CRO", "Network": "Mainnet", "RPC": "https://evm-cronos.crypto.org", "ChainID": "25", "Block_Explorer": "https://cronos.crypto.org/explorer/", "Network_Name": "Cronos"}, {"Symbol": "ELA", "Network": "Mainnet", "RPC": "https://api.elastos.io/eth", "ChainID": "20", "Block_Explorer": "https://explorer.elaeth.io/", "Network_Name": "Elastos"}, {"Symbol": "ETH", "Network": "Mainnet", "RPC": "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "ChainID": "0x1", "Block_Explorer": "https://etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "ETH", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/eth", "ChainID": "0x1", "Block_Explorer": "https://etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "ETH", "Network": "Testnet", "RPC": "https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "ChainID": "0x3", "Block_Explorer": "https://ropsten.etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "ETH", "Network": "Testnet", "RPC": "https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "ChainID": "0x4", "Block_Explorer": "https://rinkey.etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "ETH", "Network": "Testnet", "RPC": "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "ChainID": "0x5", "Block_Explorer": "https://goerli.etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "ETH", "Network": "Testnet", "RPC": "https://kovan.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "ChainID": "0x6", "Block_Explorer": "https://kovan.etherscan.io", "Network_Name": "Ethereum"}, {"Symbol": "FTM", "Network": "Mainnet", "RPC": "https://rpc.ftm.tools/", "ChainID": "0xfa", "Network_Name": "Fantom"}, {"Symbol": "FTM", "Network": "Testnet", "RPC": "https://rpc.testnet.fantom.network/", "ChainID": "0xfa2", "Network_Name": "Fantom"}, {"Symbol": "FUSE", "Network": "Mainnet", "RPC": "https://rpc.fuse.io", "ChainID": "0x7a", "Block_Explorer": "https://explorer.fuse.io/", "Network_Name": "Fuse"}, {"Symbol": "Gnosis", "Network": "Mainnet", "RPC": "https://rpc.gnosischain.com", "ChainID": "0x64", "Block_Explorer": "https://blockscout.com/xdai/mainnet/", "Network_Name": "Gnosis"}, {"Symbol": "Huobi Eco Chain", "Network": "Mainnet", "RPC": "https://http-mainnet-node.huobichain.com/", "ChainID": "128", "Block_Explorer": "https://hecoinfo.com/", "Network_Name": "Huobi Eco Chain"}, {"Symbol": "Huobi Eco Chain", "Network": "Testnet", "RPC": "https://http-testnet.hecochain.com", "ChainID": "256", "Block_Explorer": "https://testnet.hecoinfo.com/", "Network_Name": "Huobi Eco Chain"}, {"Symbol": "HOO", "Network": "Mainnet", "RPC": "https://http-mainnet.hoosmartchain.com", "ChainID": "70", "Block_Explorer": "https://hooscan.com", "Network_Name": "Hoo"}, {"Symbol": "IOTEX", "Network": "Mainnet", "RPC": "https://babel-api.mainnet.iotex.io", "ChainID": "4689", "Block_Explorer": "https://iotexscan.io/", "Network_Name": "IoTeX"}, {"Symbol": "KCS", "Network": "Mainnet", "RPC": "https://rpc-mainnet.kcc.network", "ChainID": "321", "Block_Explorer": "https://scan.kcc.network", "Network_Name": "Kucoin Chain"}, {"Symbol": "Kucoin Chain", "Network": "Testnet", "RPC": "https://rpc-testnet.kcc.network", "ChainID": "322", "Block_Explorer": "https://scan-testnet.kcc.network", "Network_Name": "Kucoin Chain"}, {"Symbol": "MATIC", "Network": "Mainnet", "RPC": "https://polygon-rpc.com", "ChainID": "0x89", "Block_Explorer": "https://explorer.matic.network/", "Network_Name": "Polygon Matic"}, {"Symbol": "MATIC", "Network": "Mainnet", "RPC": "https://matic-mainnet.chainstacklabs.com", "ChainID": "0x89", "Block_Explorer": "https://explorer.matic.network/", "Network_Name": "Polygon Matic"}, {"Symbol": "MATIC", "Network": "Testnet", "RPC": "https://rpc-mumbai.maticvigil.com", "ChainID": "0x13881", "Block_Explorer": "https://mumbai.polygonscan.com/", "Network_Name": "Polygon Matic"}, {"Symbol": "MOVR", "Network": "Mainnet", "RPC": "https://rpc.moonriver.moonbeam.network", "ChainID": "1285", "Block_Explorer": "https://blockscout.moonriver.moonbeam.network/", "Network_Name": "Moonriver"}, {"Symbol": "Nahmii", "Network": "Mainnet", "RPC": "https://l2.nahmii.io", "ChainID": "5551", "Block_Explorer": "https://explorer.nahmii.io/", "Network_Name": "Nahmii"}, {"Symbol": "Nahmii", "Network": "Testnet", "RPC": "https://l2.testnet.nahmii.io", "ChainID": "5553", "Block_Explorer": "https://explorer.testnet.nahmii.io/", "Network_Name": "Nahmii"}, {"Symbol": "NEAR", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/near", "Network_Name": "Near"}, {"Symbol": "OKT", "Network": "Mainnet", "RPC": "https://exchainrpc.okex.org", "ChainID": "66", "Block_Explorer": "https://www.oklink.com/okexchain", "Network_Name": "OKEx"}, {"Symbol": "ONE", "Network": "Mainnet", "RPC": "https://api.harmony.one", "ChainID": "0x63564c40", "Block_Explorer": "https://explorer.harmony.one", "Network_Name": "Harmony"}, {"Symbol": "ONE", "Network": "Mainnet", "RPC": "https://harmony-mainnet.chainstacklabs.com", "ChainID": "0x63564c40", "Block_Explorer": "https://explorer.harmony.one", "Network_Name": "Harmony"}, {"Symbol": "ONE", "Network": "Testnet", "RPC": "https://api.s0.b.hmny.io", "ChainID": "0x6357d2e0", "Block_Explorer": "https://explorer.harmony.one", "Network_Name": "Harmony"}, {"Symbol": "Pando", "Network": "Mainnet", "RPC": "https://eth-rpc-api.pandoproject.org/rpc", "ChainID": "398", "Block_Explorer": "https://explorer.pandoproject.org", "Network_Name": "Pando"}, {"Symbol": "BCH", "Network": "Mainnet", "RPC": "https://smartbch.fountainhead.cash/mainnet", "ChainID": "10000", "Block_Explorer": "https://www.smartscan.cash/", "Network_Name": "SmartBCH"}, {"Symbol": "SOL", "Network": "Mainnet", "RPC": "https://rpc.ankr.com/solana", "Block_Explorer": "https://solscan.io/", "Network_Name": "Solana"}, {"Symbol": "TLOS", "Network": "Mainnet", "RPC": "https://mainnet.telos.net/evm", "ChainID": "40", "Block_Explorer": "https://telos.net/", "Network_Name": "Telos"}, {"Symbol": "UBQ", "Network": "Mainnet", "RPC": "https://rpc.octano.dev", "ChainID": "8", "Block_Explorer": "https://ubiqscan.io/", "Network_Name": "Ubiq"}]

# Insert your RPC list here
def get_key_from_value(value:str)-> (str or None):
    """
    Fetches the key for a given value from the `get_rpc_js()` mapping.
    
    Parameters:
    - value: The value for which the key needs to be found.
    
    Returns:
    - The key corresponding to the value.
    """
    for i,each in enumerate(get_rpc_js().values()):
        if value == each:
            return get_keys()[i]
def get_rpc_js()->dict:
    """
    Provides a dictionary mapping of RPC parameters.
    
    Returns:
    - dict: A dictionary of RPC parameters.
    """
    return {"Network_Name":"-NETWORK_NAME-",'Network':"-NETWORK-",'Symbol':"-SYMBOL-",'ChainID':"-CHAINID-",'RPC':"-RPC-",'Block_Explorer':"-BLOCK_EXPLORER-"}
def get_keys()->list:
    """
    Fetches the keys from the `get_rpc_js()` mapping.
    
    Returns:
    - list: A list of keys.
    """
    return list(get_rpc_js().keys())
def get_rpc_layout(rpc_list:list=None,window_mgr:type(window_mgr)=window_mgr):
    rpc_list=if_default_return_obj(obj=RPCBridge().get_default_rpc_list(),default=rpc_list)
    rpc_add_global_bridge["window_mgr"]=window_mgr
    rpc_add_global_bridge["rpc_list"]=rpc_list
    network_names = list({item['Network_Name'] for item in rpc_list})
    layout = [
        [sg.Text('Network Name:'), sg.Combo(network_names, key='-NETWORK_NAME-', enable_events=True)],
        [sg.Text('Network:'), sg.Combo([], key='-NETWORK-',size=(20,1), enable_events=True)],
        [sg.Text('RPC:'), sg.Combo([], key='-RPC-',size=(20,1), enable_events=True)],
        [sg.Text('ChainID:'), sg.InputText(key='-CHAINID-',size=(20,1), disabled=True)],  # Make this an InputText to display ChainID
        [sg.Text('Block Explorer:'), sg.Combo([], key='-BLOCK_EXPLORER-',size=(20,1), enable_events=True)],
        [sg.Text('Symbol:'), sg.InputText(key='-SYMBOL-',size=(20,1), disabled=True)]  # Make this an InputText to display Symbol
    ]
    layout.append(create_row_of_buttons({"button_text":"OK","enable_event":True,"key":"-OK_RPC-"},{"button_text":"Show","enable_event":True,"key":"-SHOW_RPC-"},{"button_text":"Reset","enable_event":True,"key":"-RESET_RPC-"},{"button_text":"Exit","enable_event":True,"key":"-EXIT_RPC-"}))
    return layout
def rpc_win_while(event=None):
    event,values,window = rpc_add_global_bridge["window_mgr"].get_event(),rpc_add_global_bridge["window_mgr"].get_values(),rpc_add_global_bridge["window_mgr"].get_last_window_method()
    if event == '-NETWORK_NAME-':
        selected_name = values['-NETWORK_NAME-']
        relevant_data = [item for item in rpc_add_global_bridge["rpc_list"] if item['Network_Name'] == selected_name]
        window['-NETWORK-'].update(values=list({item['Network'] for item in relevant_data}), set_to_index=0)
        window['-RPC-'].update(values=[], set_to_index=0)
        window['-CHAINID-'].update(value='')
        window['-BLOCK_EXPLORER-'].update(values=[], set_to_index=0)
        window['-SYMBOL-'].update(value='')
    elif event == '-NETWORK-':
        selected_name = values['-NETWORK_NAME-']
        selected_network = values['-NETWORK-']
        relevant_data = [item for item in rpc_add_global_bridge["rpc_list"] if item['Network_Name'] == selected_name and item['Network'] == selected_network]
        window['-RPC-'].update(values=list({item['RPC'] for item in relevant_data}), set_to_index=0)
        window['-CHAINID-'].update(value=next((item['ChainID'] for item in relevant_data), ''))
        window['-BLOCK_EXPLORER-'].update(value=next((item['Block_Explorer'] for item in relevant_data), ''))
        window['-SYMBOL-'].update(value=next((item['Symbol'] for item in relevant_data), ''))
def Choose_RPC_Parameters_GUI(rpc_list:list=None) -> dict or None:
    rpc_list=if_default_return_obj(obj=RPCBridge().get_default_rpc_list(),default=rpc_list)
    window = window_mgr.get_new_window(args={"title":'RPC Selector',"layout":get_rpc_layout(rpc_list=rpc_list),"exit_events":["-OK_RPC-","-EXIT_RPC-"],"event_function":"rpc_win_while","suppress_raise_key_errors":False, "suppress_error_popups":False, "suppress_key_guessing":False,"finalize":True})
    values = window_mgr.while_basic(window=window)
    rpc={}
    if values:
        for each in values.keys():
            key = get_key_from_value(each)
            if key in get_keys():
                rpc[key] = values[each]
    return RPCBridge(rpc).return_rpc_js()

