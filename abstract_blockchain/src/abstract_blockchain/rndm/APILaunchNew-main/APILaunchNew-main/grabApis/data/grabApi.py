import requests
import PySimpleGUI as sg
import json
import sys
import functions as fun
import testABI as testAb
import parseFuns
import urllib
from web3.contract import ContractEvent
from web3.contract import Contract
from web3._utils.events import get_event_data
from web3 import Web3
from web3.auto import w3
import time
import datetime
import os
def changeGlob(x,y):
    globals()[x] = y
    return y
def ti():
    return time.time()
def homeIt():
    changeGlob('home',os.getcwd())
    if changeGlob('slash','/') not in home:
        changeGlob('slash','\\')
    return home,slash
def stripWeb(x):
    if 'http' in x:
        x = x.replace('https','').replace('http','')
        while x[0] in [':',slash] and len(x)>1:
            x = x[1:]
    return x.split(slash)[0]
def check_sleep(x):
    curr = ti() - float(x)
    if curr < 1.5:
        time.sleep(1.5 - curr)
    return
def getRound(x):
  last_api = fun.existJsRead('[0,0]','last_api.txt')
  check_sleep(last_api[1])
  data = urllib.request.urlopen(x).read()
  last_api[1] = ti()
  fun.pen(last_api,'last_api.txt')
  print(data)
  return data
def sites_scan(x):
    end = 0
    print(x)
    while end == 0:
        output = getRound(x)
        if output == {'status': '0', 'message': 'No records found', 'result': []}:
            return 
    if str(output['result']) == '{}':
        return 0
    try:
        js = output[x]['results']
        c = ','
        if len(curr_prices) == 0:
            c = ''
        pen(str(curr_prices).replace('}','')+c+'"'+str(x)+'":"'+str(js)+'"}','price_now.txt')
        return js
    except:
        print('scan sleeping ',x,output)
        time.sleep(20)
def sites(A):
    U = [A]
    fun.existJsRead('[0,0]','last_api.txt')
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)['result']
        changeGlob('lastRequest',time.time())
    return JS
def apiKeys(scanner):
    if scanner == 'bscscan.com':
        key = 'JYVRVFFC32H2ZSKDY1JZKNY7XV1Y5MCJHM'
    elif scanner == 'polygonscan.com':
        key = 'S6X6NY29X4ARWRVSIZJTG1PJS4IG86B3WJ'
    elif scanner == 'ftmscan.com':
        key = 'WU2C3NZAQC9QT299HU5BF7P8QCYX39W327'
    elif scanner == 'moonbeam.moonscan.io':
        key = '5WVKC1UGJ3JMWQZQAT8471ZXT3UJVFDF4N'
    else:
        key = '4VK8PEWQN4TU4T5AV5ZRZGGPFD52N2HTM1'
    return key
def chooseIt():
    global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3
    netName,chainId,rpc,nativeCurrency,explorer,scanner,w3 = chooseIt()
    netName,chainId,rpc,nativeCurrency,explorer,scanner = fun.eatAllLs([netName,chainId,rpc,nativeCurrency,explorer,scanner],[' ',''])
def getAbi(add):
    global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3
    return sites('https://api.'+str(scanner)+'/api?module=contract&action=getabi&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
def getSource(add):
    global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3
    return sites('https://api.'+str(scanner)+'/api?module=contract&action=getsourcecode&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
def shortsites(A):
    U = [A]
    for url in U:
        X = str(U[0])
        r = requests.get(X)
    return r.json()['result']
def getData(s,dot,typ,add,scanner):
    try:
        result = shortsites('http'+str(s)+'://api'+str(dot)+str(scanner)+'/api?module=contract&action='+typ+'&address='+checkSum(str(add))+'&apikey='+str(apiKeys(scanner)))
        return 'http'+str(s)+'://api'+str(dot)+str(scanner),result
    except:
      return False
def getSources(add):
    chooseIt()
    return netName,chainId,rpc,nativeCurrency,explorer,scanner,w3,sites(getSource(add))
def getRPC(js):
    if 'RPC' in js:
        return js['RPC']
    return False
def ifAnyNameInAll(js):
    net = ''
    needs = ['netName','chainId','RPC','nativeCurrency','blockExplorer','scanner']
    for i in range(0,len(needs)):
        nee = needs[i]
        if nee not in js:
            js[nee] = ''
        if nee in js:
            if js[nee] in ['',False,' ',None]:
                if net != '':
                    if nee in net:
                       js[nee] = net[nee]
            elif findAnyId(js[nee],nee) != False:
                net = findAnyId(js[nee],nee)
                if nee in net:
                   js[nee] = net[nee]
    return js
def getChainId(js):
    nee = needs[i]
    for k in range(0,len(find)):
        if getRPC(js) == find[k]['RPC']:
            return find[k]['chainId']
    return False
def getExplorer(js):
    if 'blockExplorer' in js:
        return js['blockExplorer']
    elif getScanner(js) != False:
        return 'https://'+str(getScanner(js))
    return False
def getScanner(js):
    if 'scanner' in js:
        return js['scanner']
    elif getExplorer(js) != False:
        return stripWeb(getExplorer(js))
    return False
def getNetName(js):
    if 'networkName' in js:
        return js['networkName']
    elif 'chainId' in js:
        if findAnyId(js['chainId'],'chainId') != False:
            net = findAnyId(js['chainId'],'chainId')
            return netName
    return False
def findAnyId(x,st):
    from allJs import rpcVariables
    names = rpcVariables['networks']
    for i in range(0,len(names)):
        net = rpcVariables[names[i]]
        for k in range(0,len(net)):
            if st in net[k]:
                if net[k][st] == x:
                    return net
    return False,False
def deriveFromAnyName(js):
    return deriveFrom(ifAnyNameInAll(js))
def deriveFrom(js):
    netName,chainId,rpc,nativeCurrency,explorer,scanner,w3 = js['netName'],js['chainId'],js['RPC'],js['nativeCurrency'],js['blockExplorer'],stripWeb(js['blockExplorer']),Web3(Web3.HTTPProvider(js['RPC']))
    return netName,chainId,nativeCurrency,explorer,rpc,scanner,w3
def checkSum(x):
    return w3.toChecksumAddress(x)
def tryCheckSum(x):
    try:
        y = w3.toChecksumAddress(x)
        return y
    except:
        return False
def loading(window,meter,i,k,key,msg):
    window['runAdd'].update(value=sg.one_line_progress_meter(meter, i, k-1, key,msg))
def deriveAnyInfo(add,window):
    for k in range(0,len(rpcLs)):
      loading(window,'Network Identifier',k,len(rpcLs),rpcLs[0],'checking all available RPCs for SourceCode')
      if 'RPC' in rpcLs[k] and 'blockExplorer' in rpcLs[k] and 'chainId' in rpcLs[k]:
          netName,chainId,nativeCurrency,explorer,rpc,scanner,w3 = deriveFrom(rpcLs[k])
          for c in range(0,2):
            for i in range(0,2):
              abi = getData(['','s'][c],['.','-'][i],'getabi',add,scanner)
              source = getData(['','s'][c],['.','-'][i],'getsourcecode',add,scanner)
              if source != False:
                rpcLs[k]['specs'] = source[0]
                abi,source,add,rpc = abi[1],source[1],add,rpcLs[k]
                if fun.isLs(source):
                    source = source[0]
                if source is not None:
                    if 'ContractName' in source:
                        if source['ContractName'] !='':
                            dirPath = fun.mkDirsAll([home,'infos',str(add),str(netName),rpcLs[k]['network']])
                            path = fun.crPa(dirPath,'info.json')
                            fun.pen(json.dumps({"abi":abi,"source":source,"add":add,"rpc":rpcLs[k]}),path)
                            jso = json.loads(fun.reader(path))
                            ls = ['abi','source','rpc','add']
                            for j in range(0,len(ls)):
                                fun.pen(json.dumps(jso[ls[j]]),fun.crPa(dirPath,ls[j]+'.json'))
                            contract = json.loads(fun.reader(fun.crPa(dirPath,'source.json')))['SourceCode']
                            ABI = json.loads(json.loads(fun.reader(fun.crPa(dirPath,'source.json')))['ABI'])
                            fun.pen(json.dumps(contract),fun.crPa(dirPath,'source.json'))
                            fun.pen(json.dumps(ABI),fun.crPa(dirPath,'abi.json'))
                            lsAll = parseFuns.parse_it(add,dirPath,json.dumps(contract),json.dumps(ABI),rpcLs[k])
                            jsName = str('funs,asks,call,fun_all,funcSheet').split(',')
                            for h in range(0,len(lsAll)):
                                fun.pen(lsAll[h],fun.crPa(dirPath,jsName[h]+'.py'))
                            sys.path.insert(0, dirPath)
                            import dothefunx
                            sys.path.insert(0, home)
global netName,chainId,rpc,nativeCurrency,explorer,scanner,w3,home,slash,rpcLs,window
from rpcListNew import rpcs as rpcLs
home,slash = homeIt()

