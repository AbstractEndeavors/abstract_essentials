import hashlib
import json
from web3 import Web3
import json
import json
import PySimpleGUI as psg
class Network:
    def __init__(self, rpc_data):
        self.rpc_data = rpc_data
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_data['RPC']))
        self.netName = self.rpc_data['netName']
        self.chainId = self.rpc_data['chainId']
        self.nativeCurrency = self.rpc_data['nativeCurrency']
        self.explorer = self.rpc_data['blockExplorer']
        self.scanner = self.stripWeb(self.rpc_data['blockExplorer'])
    def stripWeb(self, url):
        # Add your logic to strip the web URL
        pass
    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path, 'r') as f:
            rpc_data = json.load(f)
        return cls(rpc_data)
# Load the network data from the JSON file
def to_checksum_address(address):
    address = address.lower().replace('0x', '')
    hashed_address = hashlib.sha3_256(address.encode('utf-8')).hexdigest()
    checksum_address = '0x'
    for i, c in enumerate(address):
        if int(hashed_address[i], 16) >= 8:
            checksum_address += c.upper()
        else:
            checksum_address += c
    return checksum_address
def try_check_sum(add):
    if len(add) == 42 and add.startswith('0x'):
        return to_checksum_address(add)
    else:
        return add
def grt_curr_rpc():
    network = json.loads(reader('/home/hmmm/Documents/python_scripts/shared/crypto/web3/saved_variables/web3_all/current_rpc.json'))
rpc_data  = [{"nativeCurrency": "Arbitrum", "network": "Mainnet", "RPC": "https://rpc.ankr.com/arbitrum", "chainId": "42161", "blockExplorer": "https://arbiscan.io/", "netName": "Arbitrum"},
             {"nativeCurrency": "AVAX", "network": "Mainnet", "RPC": "https://api.avax.network/ext/bc/C/rpc", "chainId": "43114", "blockExplorer": "https://snowtrace.io", "netName": "Avalanche"},
             {"nativeCurrency": "AVAX", "network": "Mainnet", "RPC": "https://rpc.ankr.com/avalanche", "chainId": "43114", "blockExplorer": "https://snowtrace.io", "netName": "Avalanche"},
             {"nativeCurrency": "AVAX", "network": "Testnet", "RPC": "https://api.avax-test.network/ext/bc/C/rpc", "chainId": "43113", "blockExplorer": "https://testnet.snowtrace.io", "netName": "Avalanche"},
             {"nativeCurrency": "AVAX", "network": "Testnet", "RPC": "https://localhost:9650/ext/bc/C/rpc", "chainId": "43112", "blockExplorer": "https://snowtrace.io", "netName": "Avalanche"},
             {"nativeCurrency": "BNB", "network": "Mainnet", "RPC": "https://bsc-dataseed.binance.org", "chainId": "56", "blockExplorer": "https://bscscan.com", "netName": "Binance Smart Chain"},
             {"nativeCurrency": "BNB", "network": "Mainnet", "RPC": "https://rpc.ankr.com/bsc", "chainId": "56", "blockExplorer": "https://bscscan.com", "netName": "Binance Smart Chain"},
             {"nativeCurrency": "BNB", "network": "Testnet", "RPC": "https://data-seed-prebsc-1-s1.binance.org:8545", "chainId": "97", "blockExplorer": "https://testnet.bscscan.com", "netName": "Binance Smart Chain"},
             {"nativeCurrency": "CELO", "network": "Mainnet", "RPC": "https://rpc.ankr.com/celo", "chainId": "42220", "blockExplorer": "https://celoscan.com", "netName": "Celo"},
             {"nativeCurrency": "CONDOR", "network": "Testnet",  "RPC": "https::www..com","chainId": "188881", "netName": "Condor","blockExplorer": "https::www..com"},
             {"nativeCurrency": "CRO", "network": "Mainnet", "RPC": "https://evm-cronos.crypto.org", "chainId": "25", "blockExplorer": "https://cronos.crypto.org/explorer/", "netName": "Cronos"},
             {"nativeCurrency": "ELA", "network": "Mainnet", "RPC": "https://api.elastos.io/eth", "chainId": "20", "blockExplorer": "https://explorer.elaeth.io/", "netName": "Elastos"},
             {"nativeCurrency": "ETH", "network": "Mainnet", "RPC": "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "chainId": "0x1", "blockExplorer": "https://etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "ETH", "network": "Mainnet", "RPC": "https://rpc.ankr.com/eth", "chainId": "0x1", "blockExplorer": "https://etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "ETH", "network": "Testnet", "RPC": "https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "chainId": "0x3", "blockExplorer": "https://ropsten.etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "ETH", "network": "Testnet", "RPC": "https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "chainId": "0x4", "blockExplorer": "https://rinkey.etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "ETH", "network": "Testnet", "RPC": "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "chainId": "0x5", "blockExplorer": "https://goerli.etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "ETH", "network": "Testnet", "RPC": "https://kovan.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161", "chainId": "0x6", "blockExplorer": "https://kovan.etherscan.io", "netName": "Ethereum"},
             {"nativeCurrency": "FTM", "network": "Mainnet", "RPC": "https://rpc.ftm.tools/", "chainId": "0xfa", "netName": "Fantom","blockExplorer": "https::www..com"},
             {"nativeCurrency": "FTM", "network": "Testnet", "RPC": "https://rpc.testnet.fantom.network/", "chainId": "0xfa2", "netName": "Fantom","blockExplorer": "https::www..com"},
             {"nativeCurrency": "FUSE", "network": "Mainnet", "RPC": "https://rpc.fuse.io", "chainId": "0x7a", "blockExplorer": "https://explorer.fuse.io/", "netName": "Fuse"},
             {"nativeCurrency": "Gnosis", "network": "Mainnet", "RPC": "https://rpc.gnosischain.com", "chainId": "0x64", "blockExplorer": "https://blockscout.com/xdai/mainnet/", "netName": "Gnosis"},
             {"nativeCurrency": "Huobi Eco Chain", "network": "Mainnet", "RPC": "https://http-mainnet-node.huobichain.com/", "chainId": "128", "blockExplorer": "https://hecoinfo.com/", "netName": "Huobi Eco Chain"},
             {"nativeCurrency": "Huobi Eco Chain", "network": "Testnet", "RPC": "https://http-testnet.hecochain.com", "chainId": "256", "blockExplorer": "https://testnet.hecoinfo.com/", "netName": "Huobi Eco Chain"},
             {"nativeCurrency": "HOO", "network": "Mainnet", "RPC": "https://http-mainnet.hoosmartchain.com", "chainId": "70", "blockExplorer": "https://hooscan.com", "netName": "Hoo"},
             {"nativeCurrency": "IOTEX", "network": "Mainnet", "RPC": "https://babel-api.mainnet.iotex.io", "chainId": "4689", "blockExplorer": "https://iotexscan.io/", "netName": "IoTeX"},
             {"nativeCurrency": "KCS", "network": "Mainnet", "RPC": "https://rpc-mainnet.kcc.network", "chainId": "321", "blockExplorer": "https://scan.kcc.network", "netName": "Kucoin Chain"},
             {"nativeCurrency": "Kucoin Chain", "network": "Testnet", "RPC": "https://rpc-testnet.kcc.network", "chainId": "322", "blockExplorer": "https://scan-testnet.kcc.network", "netName": "Kucoin Chain"},
             {"nativeCurrency": "MATIC", "network": "Mainnet", "RPC": "https://polygon-rpc.com", "chainId": "0x89", "blockExplorer": "https://explorer.matic.network/", "netName": "Polygon Matic"},
             {"nativeCurrency": "MATIC", "network": "Mainnet", "RPC": "https://matic-mainnet.chainstacklabs.com", "chainId": "0x89", "blockExplorer": "https://explorer.matic.network/", "netName": "Polygon Matic"},
             {"nativeCurrency": "MATIC", "network": "Testnet", "RPC": "https://rpc-mumbai.maticvigil.com", "chainId": "0x13881", "blockExplorer": "https://mumbai.polygonscan.com/", "netName": "Polygon Matic"},
             {"nativeCurrency": "MOVR", "network": "Mainnet", "RPC": "https://rpc.moonriver.moonbeam.network", "chainId": "1285", "blockExplorer": "https://blockscout.moonriver.moonbeam.network/", "netName": "Moonriver"},
             {"nativeCurrency": "Nahmii", "network": "Mainnet", "RPC": "https://l2.nahmii.io", "chainId": "5551", "blockExplorer": "https://explorer.nahmii.io/", "netName": "Nahmii"},
             {"nativeCurrency": "Nahmii", "network": "Testnet", "RPC": "https://l2.testnet.nahmii.io", "chainId": "5553", "blockExplorer": "https://explorer.testnet.nahmii.io/", "netName": "Nahmii"},
             {"nativeCurrency": "NEAR", "network": "Mainnet", "RPC": "https://rpc.ankr.com/near","chainId":"0000", "netName": "Near","blockExplorer":'https://www..com'},
             {"nativeCurrency": "OKT", "network": "Mainnet", "RPC": "https://exchainrpc.okex.org", "chainId": "66", "blockExplorer": "https://www.oklink.com/okexchain", "netName": "OKEx"},
             {"nativeCurrency": "ONE", "network": "Mainnet", "RPC": "https://api.harmony.one", "chainId": "0x63564c40", "blockExplorer": "https://explorer.harmony.one", "netName": "Harmony"},
             {"nativeCurrency": "ONE", "network": "Mainnet", "RPC": "https://harmony-mainnet.chainstacklabs.com", "chainId": "0x63564c40", "blockExplorer": "https://explorer.harmony.one", "netName": "Harmony"},
             {"nativeCurrency": "ONE", "network": "Testnet", "RPC": "https://api.s0.b.hmny.io", "chainId": "0x6357d2e0", "blockExplorer": "https://explorer.harmony.one", "netName": "Harmony"},
             {"nativeCurrency": "Pando", "network": "Mainnet", "RPC": "https://eth-rpc-api.pandoproject.org/rpc", "chainId": "398", "blockExplorer": "https://explorer.pandoproject.org", "netName": "Pando"},
             {"nativeCurrency": "BCH", "network": "Mainnet", "RPC": "https://smartbch.fountainhead.cash/mainnet", "chainId": "10000", "blockExplorer": "https://www.smartscan.cash/", "netName": "SmartBCH"},
             {"nativeCurrency": "SOL", "network": "Mainnet", "RPC": "https://rpc.ankr.com/solana", "chainId": "00", "blockExplorer": "https://solscan.io/", "netName": "Solana"},
             {"nativeCurrency": "TLOS", "network": "Mainnet", "RPC": "https://mainnet.telos.net/evm", "chainId": "40", "blockExplorer": "https://telos.net/", "netName": "Telos"},
             {"nativeCurrency": "UBQ", "network": "Mainnet", "RPC": "https://rpc.octano.dev", "chainId": "8", "blockExplorer": "https://ubiqscan.io/", "netName": "Ubiq"}]
rpc_now = rpc_data
import PySimpleGUI as sg
import json
def filter_rpc_data(network, rpc_data):
    return [item for item in rpc_data if item['network'] == network]
def main():
    sg.theme('BlueMono') 
    layout = [
        [sg.Text('Net Name'), sg.Combo(sorted(list(set([item['netName'] for item in rpc_data]))), key='netName', enable_events=True)],
        [sg.Text('Network'), sg.Combo(sorted(list(set([item['network'] for item in rpc_data]))), key='network', enable_events=True)],
        [sg.Text('RPC'), sg.Combo(sorted(list(set([item['RPC'] for item in rpc_data]))), key='RPC', enable_events=True)],
        [sg.Text('Chain ID'), sg.Combo(sorted(list(set([item['chainId'] for item in rpc_data]))), key='chainId')],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]
    window = sg.Window('RPC Selector', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'network':
            filtered_data = filter_rpc_data(values[event], rpc_data)
            net_names = [item['netName'] for item in filtered_data]
        elif event == 'netName':
            selected_item = next(item for item in rpc_data if item['netName'] == values[event])
            chain_id = [selected_item['chainId']]
            RPC= [selected_item['RPC']]
            window['chainId'].update(values=chain_id)
            window['RPC'].update(values=RPC)
        elif event == 'OK':
            selected_network = next(item for item in rpc_data if item['netName'] == values['netName'] and item['chainId'] == values['chainId'] and item['RPC'] == values['RPC'])
            print(selected_network)
            break
    window.close()
if __name__ == "__main__":
    main()
