import functions as ff
import web3
from web3 import Web3, HTTPProvider
import networkChoose as choose
import json
def homeIt():
    changeGlob('home',os.getcwd())
    slash = '//'
    if '//' not in str(home):
        slash = '/'
    changeGlob('slash',slash)
    return home,slash
def changeGlob(x,v):
    globals()[x] = v
def getKeys(js):
    lsN = []
    for key, value in js.items():
        lsN.append(key)
    pen(lsN,'rpckeys.txt')
def tryCheckSum(x):
    try:
        y = w3.toChecksumAddress(x)
        return y
    except:
        return False
def checkIfDud(x):
    if  x != None:
        if len(x)>0:
            if len(x) >1:
                  return x
    return False
def countIt(x,y):
    if y not in x:
        return 0
    return int((len(x)-len(x.replace(y,'')))/len(y))
def eatX(x):
    if checkIfDud(x) != False:
        while x[-1] == slash and len(x)>1:
            x = x[:-1]
    return x
def eatY(y):
    if checkIfDud(y) != False:
        while y[0] == slash and len(y) >1:
            y[1:]
    return y
def createPath(x,y):
    return eatX(x)+'/'+eatY(y)
def createInps(ls):
    n = '('
    for i in range(0,len(ls)):
        n = n + ls[i]+ ','
    n = n.replace(' ','_').replace('[]','ls') + ')'
    return n.replace(',)',')')
def stripWeb(x):
    if 'http' in x:
        x = x.replace('https','').replace('http','')
        while x[0] in [':',slash] and len(x)>1:
            x = x[1:]
    return x.split(slash)[0]
def extractRPCdata(js):
    kes = ['nativeCurrency', 'network', 'RPC', 'chainId', 'blockExplorer']
    for i in range(0,len(kes)):
        if kes[i] not in js:
            js[kes[i]] = ""
    changeGlob('nativeCurrency',js['nativeCurrency'])
    changeGlob('network',js['network'])
    changeGlob('blockExplorer',js['blockExplorer'])
    changeGlob('RPC',js['RPC'])
    changeGlob('chainId',js['chainId'])
    changeGlob('scanner',stripWeb(js['blockExplorer']))
    return nativeCurrency,network,RPC,chainId,blockExplorer,scanner,Web3(Web3.HTTPProvider(js['RPC']))
def getTypes(varis):
    spl,n = str(varis)[1:-1].split(','),''
    for k in range(0,len(spl)):
        typ = spl[k].split('__')[0]
        if 'int' in  typ:
            n = n + 'int('+str(spl[k])+'),'
        elif 'bytes' in typ:
            n = n + 'kek('+str(spl[k])+'),'
        else:
            n = n + 'str('+str(spl[k])+'),'
    return '('+n[:-1]+')'
def parse_it(add,path,contract,abi,main):
    nativeCurrency,network,RPC,chainId,explorer,scanner,w3 = extractRPCdata(main)
    ff.pen(add,'currInfo.txt')
    import funGet as fun
    js = json.loads(fun.getFuns(path,contract,abi))
    #beg = "from web3 import Web3\nimport sys\nimport os\nhome = os.getcwd()\nimport json\nsys.path.insert(0, '"+createPath(home,'walls')+"')\nimport priv_key as priv\ndef homeIt():\n\tchangeGlob('home',os.getcwd())\n\tslash = '//'\n\tif '//' not in str(home):\n\t\tslash = '/'\n\t\tchangeGlob('slash',slash)\n\treturn home,slash\ndef pen(paper, place):\n\twith open(place, 'w') as f:\n\t\tf.write(str(paper))\n\t\tf.close()\n\t\treturn\ndef isHex(x):\n\ttry:\n\t\tz = x.hex()\n\t\treturn True\n\texcept:\n\t\treturn False\ndef printHex(x):\n\tif isHex(x):\n\t\treturn x.hex()\n\treturn x\n\treturn text\ndef changeGlob(x,v):\n\tglobals()[x] = v\ndef readerC(file):\n\twith open(file,'r' ,encoding=^*^utf-8-sig^*^) as f:\n\t\ttext = f.read()\n\t\treturn text\n".replace('^*^','"')
    #end = '\nglobal netName,chainId,rpc,nativeCurrency,explorer,scanner,w3,nonce\nABI = '+"'"+ff.readerC(ff.crPa([path,"ABI.json"]))+"'"+'\nchangeGlob("jsInfo",'+str(main)+")\nchangeGlob('chainId',jsInfo['chainId'])\nchangeGlob('scanner',jsInfo['blockExplorer'])\nchangeGlob('w3',Web3(Web3.HTTPProvider(jsInfo['RPC'])))\nadd = w3.toChecksumAddress('"+add+"')\ncont = w3.eth.contract(add,abi = ABI)\naccount_1 = w3.eth.account.privateKeyToAccount(priv.p)\nnonce = w3.eth.getTransactionCount(account_1.address)"
    symbol = 'cont'
    call = []
    asks = []
    fun_sheet = ''
    view_sheet = 'def view_all():\n\t'
    js['varis'] = {}
    funs = js['funs']
    funsWhole =  js['function']
    funnames = funsWhole['names']
    lsN = ['view_all()']
    for i in range(0,len(funnames)):
        name = str(funnames[i])
        varis = str(createInps(funsWhole[name]['inputs']))
        js['varis'][name] = varis[1:-1]
        wholeFun = str(name + varis)
        lsN.append(wholeFun)
        #if funsWhole[name]['stateMutability'] not in ['internal','private','external'] and name not in js['modified']['onlyOwner()']:
        #    asks.append(wholeFun)
        #    fun_sheet = fun_sheet + 'def '+name+varis+':\n\tx = cont.functions.'+wholeFun+'.call()\n\tpen(x,"ask.txt")\n\tprint("'+name+'"," is ",x)\n\treturn x\n'
        if varis == '()' and name in js['view']:
            view_sheet = view_sheet +  'print("'+name+'",":",(cont.functions.'+wholeFun+'.call()))\n\t'
            fun_sheet = fun_sheet + 'def '+wholeFun+':\n\ttx = cont.functions.'+name+varis+'.call()\n\tprint("'+str(name)+' ="+str(tx))\n\treturn tx\n'
        else:
            call.append(wholeFun)
            vLs = str(varis)[1:-1]+'='+'ls\n\t'
            if countIt(varis,',') == 0:
                vLs = ''
                if len(str(varis)[1:-1]) != 0:
                    vLs = str(varis)[1:-1]+'='+'ls[0]\n\t'
            fun_sheet = fun_sheet + 'def '+str(name)+'(ls):\n\t'+str(vLs)+'tx = cont.functions.'+name+getTypes(varis)+".buildTransaction({'gasPrice': avgGasPriceEst(),'gas':web3.eth.estimateGas({'to': w3.toChecksumAddress(add), 'from': w3.toChecksumAddress(account_1.address), 'value': 0}),'from': account_1.address,'nonce': nonce,'chainId': int(chainId)})\n\tprint(tx)\n\treturn tx\n"
    if view_sheet == 'def view_all():\n\t':
        view_sheet = 'def view_all():\n\tprint()'
    fun_sheet = fun_sheet+'\ndef getDefVaris(na):\n\tjs = '+str(js['varis'])+'\n\treturn js[na].split(",")\n' +view_sheet
    get_em = [asks,call]
    fun_all = []
    for k in range(0,len(get_em)):
        for i in range(0,len(get_em[k])):
            n = 'funs.'+get_em[k][i].replace('[]','ls').replace(' ,',',').replace(', ',',').replace(' ','_')
            fun_all.append(n)
    fun_sheet = ff.reader('functionTemplate.txt').replace('^^^^insertABI^^^^',"json.loads('"+str(abi)+"')").replace('^^^^insertFunctions^^^^',fun_sheet).replace('^^^^insertListOfFunctions^^^^',str(lsN)[1:-1]).replace('^^^^insertnativeCurrency^^^^','"'+nativeCurrency+'"').replace('^^^^insertNetwork^^^^','"'+network+'"').replace('^^^^insertRPC^^^^','"'+RPC+'"').replace('^^^^insertChainId^^^^',chainId).replace('^^^^insertBlockExplorer^^^^','"'+blockExplorer+'"').replace('^^^^insertNetworkName^^^^','"'+nativeCurrency+'"').replace('^^^^insertAddress^^^^',str('"'+add+'"'))
    ff.pen('import funcSheet as func\nwhile True:\n\ttry:\n\t\tfunc.hubbub()\n\texcept Exception as e:\n\t\tprint(e)',ff.crPa(path,'dothefunx.py'))
    return funs,asks,call,fun_all,fun_sheet
home,slash = ff.homeIt()
