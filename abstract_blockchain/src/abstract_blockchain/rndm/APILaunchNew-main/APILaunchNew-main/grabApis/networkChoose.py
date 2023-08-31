import web3
from web3 import Web3, HTTPProvider
import os
import json
def currPath():
    return os.getcwd()
def homeIt():
    curr = currPath()
    slash = '//'
    if '//' not in str(curr):
        slash = '/'
    changeGlob('slash',slash)
    changeGlob('home',curr)
    return home,slash
def changeGlob(x,v):
    globals()[x] = v
def findItAlph(x,ls):
    for i in range(0,len(ls)):
        if x == ls[i]:
            return i
def takeInp(ls):
    lsN = []
    for i in range(0,len(ls)):
        lsN.append(str(input(ls[i])))
    return lsN
def create_ask(x,y):
        n = y + '\n0) to exit\n1) custom\n\n\n'
        alph = createAlph(len(x))
        alphGood = ['0','1']
        for i in range(0,len(x)):
        	alphGood.append(alph[i])
        	n = n + str(alph[i]) + ') '+str(x[i])+'\n'
        while True:
        	ask = input(n)
        	if ask in alphGood:
        		if ask == str(0):
        		    return "back"
        		if ask == str(1):
        		    return "custom"
        		i = findItAlph(str(ask),alph)
        		return x[i],i
        	print('looks like you entered an input that was not selectable,please re-input your selection')
def createAlph(i):
    k = int(i/int(26) + 1)
    alph = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
    alphNew = []
    alLen = i
    for l in range(0,k):
        lenNow = i
        if i>int(26):
            lenNow = int(26)
        for c in range(0,lenNow):
            n = alph[c]
            for ck in range(0,l):
                n = n + alph[c]
            alphNew.append(n)
        i -=1
    return alphNew
def longestMul(ls,ls2):
    lsN = []
    for i in range(0,len(ls2)):
        lsN.append([])
        for k in range(0,len(ls)):
            lsN[i].append(ls[k][ls2[i]])
    for i in range(0,len(lsN)):
        lsN[i] = spaceEmOut(lsN[i])
        for k in range(0,len(ls)):
            ls[k][ls2[i]] = lsN[i][k]
    return ls
def spaceEmOut(ls):
    sp = ' '
    long = getLongest(ls)
    for i in range(0,len(ls)):
        if i != long:
            while len(ls[i]) < len(ls[long]):
                ls[i] = ls[i] + sp
    return ls
def createNewNetwork():
    var = ['netName','chainId','RPC','nativeCurrency','blockExplorer','scanner']
    askLs = ['please enter the token name:\n','please enter the native currency abbreviatioin:\n','please enter the RPC address:\n','please enter the chain ID:\n','please enter the block explorer address']
    lsN = takeInp(askLs)
    js = {}
    for i in range(1,len(lsN)):
        js[var[i]] = lsN[i]
    return js,lsN[0]
def cleanVars(ls):
    lsN = []
    for i in range(0,len(ls)):
        stop = False
        lsN.append(str(ls[i]))
        n = 0
        for k in range(0,len(ls[i])):
            if ls[i][k] in [' ','\t','\n']:
                n = k
            else:
                stop = True
            if stop == True and ls[i][k] not in [' ','\t','\n']:
                lsN[i] = ls[i][n:k+1]
    return lsN
def allNets():
    return {'names': ['Arbitrum', 'Avalanche', 'Binance Smart Chain', 'Celo', 'Condor', 'Cronos', 'Elastos', 'Ethereum', 'Fantom', 'Fuse', 'Gnosis', 'Huobi Eco Chain', 'Hoo', 'IoTeX', 'Kucoin Chain', 'Polygon Matic', 'Moonriver', 'Nahmii', 'Near', 'OKEx', 'Harmony', 'Pando', 'SmartBCH', 'Solana', 'Telos', 'Ubiq'], 'Arbitrum': [{'nativeCurrency': 'Arbitrum', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/arbitrum', 'chainId': '42161', 'blockExplorer': 'https://arbiscan.io/'}], 'Avalanche': [{'nativeCurrency': 'AVAX', 'network': 'Mainnet', 'RPC': 'https://api.avax.network/ext/bc/C/rpc', 'chainId': '43114', 'blockExplorer': 'https://snowtrace.io'}, {'nativeCurrency': 'AVAX', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/avalanche', 'chainId': '43114', 'blockExplorer': 'https://snowtrace.io'}, {'nativeCurrency': 'AVAX', 'network': 'Testnet', 'RPC': 'https://api.avax-test.network/ext/bc/C/rpc', 'chainId': '43113', 'blockExplorer': 'https://testnet.snowtrace.io'}, {'nativeCurrency': 'AVAX', 'network': 'Testnet', 'RPC': 'https://localhost:9650/ext/bc/C/rpc', 'chainId': '43112', 'blockExplorer': 'https://snowtrace.io'}], 'Binance Smart Chain': [{'nativeCurrency': 'BNB', 'network': 'Mainnet', 'RPC': 'https://bsc-dataseed.binance.org', 'chainId': '56', 'blockExplorer': 'https://bscscan.com'}, {'nativeCurrency': 'BNB', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/bsc', 'chainId': '56', 'blockExplorer': 'https://bscscan.com'}, {'nativeCurrency': 'BNB', 'network': 'Testnet', 'RPC': 'https://data-seed-prebsc-1-s1.binance.org:8545', 'chainId': '97', 'blockExplorer': 'https://testnet.bscscan.com'}], 'Celo': [{'nativeCurrency': 'CELO', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/celo', 'chainId': '42220', 'blockExplorer': 'https://celoscan.com'}], 'Condor': [{'nativeCurrency': 'CONDOR', 'network': 'Testnet', 'chainId': '188881'}], 'Cronos': [{'nativeCurrency': 'CRO', 'network': 'Mainnet', 'RPC': 'https://evm-cronos.crypto.org', 'chainId': '25', 'blockExplorer': 'https://cronos.crypto.org/explorer/'}], 'Elastos': [{'nativeCurrency': 'ELA', 'network': 'Mainnet', 'RPC': 'https://api.elastos.io/eth', 'chainId': '20', 'blockExplorer': 'https://explorer.elaeth.io/'}], 'Ethereum': [{'nativeCurrency': 'ETH', 'network': 'Mainnet', 'RPC': 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chainId': '0x1', 'blockExplorer': 'https://etherscan.io'}, {'nativeCurrency': 'ETH', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/eth', 'chainId': '0x1', 'blockExplorer': 'https://etherscan.io'}, {'nativeCurrency': 'ETH', 'network': 'Testnet', 'RPC': 'https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chainId': '0x3', 'blockExplorer': 'https://ropsten.etherscan.io'}, {'nativeCurrency': 'ETH', 'network': 'Testnet', 'RPC': 'https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chainId': '0x4', 'blockExplorer': 'https://rinkey.etherscan.io'}, {'nativeCurrency': 'ETH', 'network': 'Testnet', 'RPC': 'https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chainId': '0x5', 'blockExplorer': 'https://goerli.etherscan.io'}, {'nativeCurrency': 'ETH', 'network': 'Testnet', 'RPC': 'https://kovan.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chainId': '0x6', 'blockExplorer': 'https://kovan.etherscan.io'}], 'Fantom': [{'nativeCurrency': 'FTM', 'network': 'Mainnet', 'RPC': 'https://rpc.ftm.tools/', 'chainId': '0xfa'}, {'nativeCurrency': 'FTM', 'network': 'Testnet', 'RPC': 'https://rpc.testnet.fantom.network/', 'chainId': '0xfa2'}], 'Fuse': [{'nativeCurrency': 'FUSE', 'network': 'Mainnet', 'RPC': 'https://rpc.fuse.io', 'chainId': '0x7a', 'blockExplorer': 'https://explorer.fuse.io/'}], 'Gnosis': [{'nativeCurrency': 'Gnosis', 'network': 'Mainnet', 'RPC': 'https://rpc.gnosischain.com', 'chainId': '0x64', 'blockExplorer': 'https://blockscout.com/xdai/mainnet/'}], 'Huobi Eco Chain': [{'nativeCurrency': 'Huobi Eco Chain', 'network': 'Mainnet', 'RPC': 'https://http-mainnet-node.huobichain.com/', 'chainId': '128', 'blockExplorer': 'https://hecoinfo.com/'}, {'nativeCurrency': 'Huobi Eco Chain', 'network': 'Testnet', 'RPC': 'https://http-testnet.hecochain.com', 'chainId': '256', 'blockExplorer': 'https://testnet.hecoinfo.com/'}], 'Hoo': [{'nativeCurrency': 'HOO', 'network': 'Mainnet', 'RPC': 'https://http-mainnet.hoosmartchain.com', 'chainId': '70', 'blockExplorer': 'https://hooscan.com'}], 'IoTeX': [{'nativeCurrency': 'IOTEX', 'network': 'Mainnet', 'RPC': 'https://babel-api.mainnet.iotex.io', 'chainId': '4689', 'blockExplorer': 'https://iotexscan.io/'}], 'Kucoin Chain': [{'nativeCurrency': 'KCS', 'network': 'Mainnet', 'RPC': 'https://rpc-mainnet.kcc.network', 'chainId': '321', 'blockExplorer': 'https://scan.kcc.network'}, {'nativeCurrency': 'Kucoin Chain', 'network': 'Testnet', 'RPC': 'https://rpc-testnet.kcc.network', 'chainId': '322', 'blockExplorer': 'https://scan-testnet.kcc.network'}], 'Polygon Matic': [{'nativeCurrency': 'MATIC', 'network': 'Mainnet', 'RPC': 'https://polygon-rpc.com', 'chainId': '0x89', 'blockExplorer': 'https://explorer.matic.network/'}, {'nativeCurrency': 'MATIC', 'network': 'Mainnet', 'RPC': 'https://matic-mainnet.chainstacklabs.com', 'chainId': '0x89', 'blockExplorer': 'https://explorer.matic.network/'}, {'nativeCurrency': 'MATIC', 'network': 'Testnet', 'RPC': 'https://rpc-mumbai.maticvigil.com', 'chainId': '0x13881', 'blockExplorer': 'https://mumbai.polygonscan.com/'}], 'Moonriver': [{'nativeCurrency': 'MOVR', 'network': 'Mainnet', 'RPC': 'https://rpc.moonriver.moonbeam.network', 'chainId': '1285', 'blockExplorer': 'https://blockscout.moonriver.moonbeam.network/'}], 'Nahmii': [{'nativeCurrency': 'Nahmii', 'network': 'Mainnet', 'RPC': 'https://l2.nahmii.io', 'chainId': '5551', 'blockExplorer': 'https://explorer.nahmii.io/'}, {'nativeCurrency': 'Nahmii', 'network': 'Testnet', 'RPC': 'https://l2.testnet.nahmii.io', 'chainId': '5553', 'blockExplorer': 'https://explorer.testnet.nahmii.io/'}], 'Near': [{'nativeCurrency': 'NEAR', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/near'}], 'OKEx': [{'nativeCurrency': 'OKT', 'network': 'Mainnet', 'RPC': 'https://exchainrpc.okex.org', 'chainId': '66', 'blockExplorer': 'https://www.oklink.com/okexchain'}], 'Harmony': [{'nativeCurrency': 'ONE', 'network': 'Mainnet', 'RPC': 'https://api.harmony.one', 'chainId': '0x63564c40', 'blockExplorer': 'https://explorer.harmony.one'}, {'nativeCurrency': 'ONE', 'network': 'Mainnet', 'RPC': 'https://harmony-mainnet.chainstacklabs.com', 'chainId': '0x63564c40', 'blockExplorer': 'https://explorer.harmony.one'}, {'nativeCurrency': 'ONE', 'network': 'Testnet', 'RPC': 'https://api.s0.b.hmny.io', 'chainId': '0x6357d2e0', 'blockExplorer': 'https://explorer.harmony.one'}], 'Pando': [{'nativeCurrency': 'Pando', 'network': 'Mainnet', 'RPC': 'https://eth-rpc-api.pandoproject.org/rpc', 'chainId': '398', 'blockExplorer': 'https://explorer.pandoproject.org'}], 'SmartBCH': [{'nativeCurrency': 'BCH', 'network': 'Mainnet', 'RPC': 'https://smartbch.fountainhead.cash/mainnet', 'chainId': '10000', 'blockExplorer': 'https://www.smartscan.cash/'}], 'Solana': [{'nativeCurrency': 'SOL', 'network': 'Mainnet', 'RPC': 'https://rpc.ankr.com/solana', 'blockExplorer': 'https://solscan.io/'}], 'Telos': [{'nativeCurrency': 'TLOS', 'network': 'Mainnet', 'RPC': 'https://mainnet.telos.net/evm', 'chainId': '40', 'blockExplorer': 'https://telos.net/'}], 'Ubiq': [{'nativeCurrency': 'UBQ', 'network': 'Mainnet', 'RPC': 'https://rpc.octano.dev', 'chainId': '8', 'blockExplorer': 'https://ubiqscan.io/'}]}
def mains():
    while True:
        custom = False
        from web3 import Web3
        global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3
        hashs_js = ''
        last_api = [0,0]
        scan = ['avax','polygon','ethereum','cronos_test','optimism','binance']
        choose = allNets()
        ans = create_ask(choose['names'],'which network would you like to choose?')
        netName = choose['names'][ans[1]]
        main = choose[netName]
        if netName == 'custom':
            main,netName = createNewNetwork()
            custom = True
        if netName != 'back':
            if custom == False:
                if len(main) >1:
                    stuff = ['chainId','RPC','nativeCurrency','blockExplorer']
                    lsNL = longestMul(main,stuff)
                    lsN = []
                    for i in range(0,len(main)):
                        n = ''
                        for k in range(0,len(stuff)):
                             n = n +str(stuff[k])+': '+str(main[i][stuff[k]])+', '     
                        lsN.append(n)
                    ans2 = create_ask(lsNL,'looks like there were a few options, which would you like to choose?')
                    main = choose[netName][ans2[1]]
            if isLs(main):
                main = main[0]
            chainId,rpc,nativeCurrency,blockExplorer,scanner,w3 = main['chainId'],main['RPC'],main['nativeCurrency'],main['blockExplorer'],stripWeb(main['blockExplorer']),Web3(Web3.HTTPProvider(main['RPC']))
            netName,chainId,rpc,nativeCurrency,blockExplorer,scanner = cleanVars([netName,chainId,rpc,nativeCurrency,blockExplorer,scanner])
            return netName,chainId,rpc,nativeCurrency,blockExplorer,scanner,w3
def get_abi():
    return f.sites('https://'+str(scanners)+'/api?module=contract&action=getabi&address='+str(add)+'&apikey='+str(api_key()))
global netName,chainId,rpc,nativeCurrency,blockExplorer,scanner,w3
home,slash = homeIt()
