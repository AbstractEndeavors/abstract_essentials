import json
import functions as fun
def getKey(js):
    lsN = []
    for key, value in js.items():
        lsN.append(str(key))
    return lsN
def eatIt(x):
    for i in range(0,len(x)):
        if x[0] not in [' ','\t','n','']:
            return x 
        x = x[1:]
    return x
def ifIt(k,lsN):
        return ls
def ifThen(n):
        ls = ['type','name','inputs','payable','stateMutability','output']
        
        for i in range(0,len(ls)):
                if ls[i] in n and ls[i] != False :
                        lsN.append(n[ls[i]])
        n = ''
        for i in range(0,len(lsN)):
              n = n + ifIt(i,lsN)
        return lsN
def ifNoJs(js,x):
    if x not in js:
        js[x] = {}
    return(js)
def ifNols(js,x):
    if x not in js:
        js[x] = []
    return(js)
def ifNoApp(ls,x):
    if x not in ls:
        ls.append(x)
    return(ls)
def ifIn(x,y):
        if y in x:
                return True
        return False
def ifLen(x,y):
        if y not in x:
                return ''
        if len(x[y])>0:
                return True
        return False
def iLen(i,x):
        if len(x) != i + 1:
                return ' , '
        return ') '
def tOf(x,y):
        if y not in x:
                return ''
        if x[y] == False:
                return ''
        return y
def addItStr(x,y) :
    return str(x) + str(y)
def getInp(x,js):
        n = ''
        if ifLen(x,'type') and ifIn(x,'type'):
                n = n + x['type']
                type = x['type']
                js = ifNoJs(js,type)
                js[type] = ifNols(js[type],'names')
        if ifLen(x,'name') and ifIn(x,'name'):
                name = x['name']
                n = n+' '+name+'('
                js[type]['names'] = ifNoApp(js[type]['names'],name)
                js[type] = ifNoJs(js[type],name)
        else:
            name = 'NA'
            js[type] = ifNoJs(js[type],'NA')
        js[type][name]['inputs'] = []
        if ifLen(x,'inputs') and ifIn(x,'inputs'):
                for i in range(0,len(x['inputs'])):
                        inp = ''
                        if ifLen(x['inputs'][i],'type') and ifIn(x['inputs'][i],'type'):
                                inp = addItStr(inp,x['inputs'][i]['type'])
                        if ifLen(x['inputs'][i],'name') and ifIn(x['inputs'][i],'name'):
                                inp = addItStr(inp,' '+x['inputs'][i]['name'])
                        js[type][name]['inputs'].append(inp)
                        n = addItStr(n,inp+',')
        n = addItStr(n, ') '+tOf(x,'payable')+' ')
        js[type][name]['stateMutability'] = 'public'
        if ifLen(x,'stateMutability') and ifIn(x,'stateMutability'):
                n = addItStr(n,x['stateMutability'])
                js[type][name]['stateMutability'] = x['stateMutability']
        js[type][name]['outputs'] = []
        if ifLen(x,'outputs') and ifIn(x,'outputs'):
                 n = addItStr(n,' returns(')
                 for i in range(0,len(x['outputs'])):
                         out = ''
                         if ifLen(x['outputs'][i],'type') and ifIn(x['outputs'][i],'type'):
                                out = addItStr(out,x['outputs'][i]['type'])
                         if ifLen(x['outputs'][i],'name') and ifIn(x['outputs'][i],'name'):
                               out = addItStr(out,x['outputs'][i]['name'])
                         js[type][name]['outputs'].append(out)
                         n = addItStr(n,out+',')
                 n = n + ')'
        n = n+ ' {}'
        return js,n
def getFuns(path):
        contract = fun.reader(path.replace('ABI.json','SourceCode.json')).replace('\n','').replace('function','\nfunction').replace('{','\n{').split('\n')
        js = {'funs':[],'modified':{'onlyOwner()':[]}}
        for i in range(0,len(contract)):
            if 'onlyOwner' in contract[i] and 'function' in contract[i]:
                js['modified']['onlyOwner()'].append(contract[i].split('function ')[1].split('(')[0])
        abi = json.loads(str(fun.reader(path)))
        lsN = []
        for i in range(0,len(abi)):
            ab = abi[i]
            js,func = getInp(ab,js)

            
            if ifLen(ab,'type') and ifIn(ab,'type'):
                if ab['type'] == 'function':     
                    js['funs'].append(func.replace(',)',')').replace('  ',' '))
        fun.pen(js,'allwallvar.json')
        return js,js['funs']
def getFuns2(abi,contract,dirPath):
        #contract = fun.reader(path).replace('function','\nfunction').replace('{','\n{').split('\n')
        js = {'funs':[],'modified':{'onlyOwner()':[]}}
        for i in range(0,len(contract)):
            if 'onlyOwner' in contract[i] and 'function' in contract[i]:
                js['modified']['onlyOwner()'].append(contract[i].split('function ')[1].split('(')[0])
        #abi = json.loads(str(fun.reader(path)))
        lsN = []
        for i in range(0,len(abi)):
            ab = abi[i]
            js,func = getInp(ab,js)

            
            if ifLen(ab,'type') and ifIn(ab,'type'):
                if ab['type'] == 'function':     
                    js['funs'].append(func.replace(',)',')').replace('  ',' '))
        fun.pen(js,fun.crPa(dirPath,'allwallvar.json'))
        return js,js['funs']
def testTxn(ABI,funs):
    names =ABI['function']['names']
    for i in range(0,len(names)):
        if ABI['function'][names[i]]['stateMutability'] == 'nonpayable':
             print('cont.functions.'+names[i]+'('+str(ABI['function'][names[i]]['inputs'])[1:-1].replace("'",'')+').buildTransaction({"gasPrice": 60000000000,"gas":2935824,"from": account_1.address,"nonce": w3.eth.getTransactionCount(account_1.address)})'.replace("'",''))
        if ABI['function'][names[i]]['stateMutability'] == 'view':
            print('cont.functions.'+names[i]+'('+str(ABI['function'][names[i]]['inputs'])[1:-1]+').call()')



