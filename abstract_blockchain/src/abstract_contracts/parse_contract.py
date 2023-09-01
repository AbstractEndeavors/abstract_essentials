import json
import os
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def pen(paper, place):
    with open(place, 'w') as f:
        f.write(str(paper))
        f.close()
def changeGlob(x,v):
    globals()[x] = v
def readLinesSpec(x):
    lsN = []
    lines = x.split('\n')
    for i in range(0,len(lines)):
        lines[i] = eatOuterMod(lines[i],['\n','\t',' ','']).replace('\n','')
        if lines[i] not in ['\n',' \n','',' ','\t']  and len(str(eatAllMod(lines[i],['\n','\t',' ','/',';','']))) != 0:
            lsN.append(lines[i]+'\n')
    return lsN
def lsChangeGlob(x,y):
    for i in range(0,len(x)):
        changeGlob(x[i],y[i])

def adSt(x,y):
    return str(x)+str(y)
def lsCheck(x,ls):
    for i in range(0,len(ls)):
        if x == ls[i]:
            return True
    return False
def currIs(x,ls):
    for i in range(0,len(ls)):
        if x[:len(ls[i])] == ls[i]:
            return x[len(ls[i]):]
    return False
def currIsNeg(x,ls):
    for i in range(0,len(ls)):
        if x[len(x)-len(ls[i]):] == ls[i]:
            return x[:len(x)-len(ls[i])] 
    return False
def eatInner(x,ls):
    z = x
    for i in range(0,len(x)):
        if currIs(z,ls) == False:
            return z
        else:
            z = currIs(z,ls)
    return z
def eatOuter(x,ls):
    z = x
    for i in range(0,len(x)):
        if currIsNeg(z,ls) == False:
            input(z)
            return z
        else:
            z = currIsNeg(z,ls)

    return z
def eatAll(x,ls):
    y = eatInner(x,ls)
    z = eatOuter(y,ls)
    return z
def countIt(x,y):
    if y in x:
        return int((len(x)-len(x.replace(y,'')))/len(y))
    return int(0)
def getEnclosed(x,ls):
    if type(x) is not list:
        x = [x]
    z = ''
    lsN = []
    countLs = [int(0),int(0)]
    for i in range(0,len(x)):
        line = x[i]
        zN = ''
        for j in range(0,len(line)):
            li = line[j]
            zN = zN+li
            if li in ls:
                if countLs[0] == 0:
                    z = ls[0]
                    
                    lsN = []
                countLs[findIt(li,ls)] += 1
                if countLs[0] == countLs[1]:
                    lsN.append(zN)
                    z = z + zN
                    return lsN,z
        z = z + zN
        lsN.append(line)
    
def findIt(x,ls):
    for i in range(0,len(ls)):
        if x == ls[i]:
            return i
    return False
def getBrackDiff():
    return lsBrack[0]-lsBrack[1]
def trackTabs(x):
    ls = ['{','}']
    found = findIt(x,['{','}'])
    if found != False:
        lsBrack[found] += 1
        lsBrack[2] = getAsMany('\t',getBrackDiff())
def getAsMany(x,k):
    z = ''
    for i in range(0,k):
        z = adSt(z,x)
    return z
def getCurr(ls):
    if len(ls) >0:
        return ls[-1]
    return None
def removeFirst(x,y):
    if y in x:
        return x.replace(x.split(y)[0]+y,''),x.split(y)[0]
    return '',x
def checkSyntax(x):
    names = syntax['names']
    for i in range(0,len(names)):
            name = names[i]
            for j in range(0,len(syntax[name])):
                now = syntax[name][j]
                if x == now:
                    return name
    return False
def checkNames(x):
    ls = ['interface','abstract','library','contract']
    for i in range(0,len(ls)):
        if 'names' not in lineTrack:
            lineTrack[ls[i]] = {'names':[]}
        if x in lineTrack[ls[i]]['names']:
            return ls[i]
    return False
def checkDeclared(x):
    if x in lineTrack['declared']:
        return True
    return False
def linesToString(ls):
    all = ''
    for i in range(0,len(ls)):
        all = all + ls[i]
    return all
def checkCurr(n):
    trackTabs(n)
    add = lsBrack[2]
    if n == ' ':
        #lineTrack['currLineChop'],chop = #removeFirst(lineTrack['currLineChop'],' ')
        chop = eatAll(lineTrack['newLine'][1:],[' ','','\t','\n'])
        lineTrack['currPhrase'] = chop+n
        currLineLs.append(lineTrack['currLineChop'])
        lineTrack['currLineAttrib'].append(False)
        if lsCheck(chop,heads) != False:
            lineTrack['currLineAttrib'][-1] = lsCheck(chop,heads)
            lineTrack[lsCheck(chop,heads)]['names'][-1] = chop
        if lsCheck(chop,heads) != False:
            lineTrack['currLineAttrib'][-1] = lsCheck(chop,heads)
            lineTrack[lsCheck(chop,heads)]['names'][-1] = chop
        if lineTrack['currLineAttrib'][-1] == False:
            lineTrack['currLineAttrib'][-1] = lsCheck(chop,subHeads)
            if lsCheck(chop,subHeads) !=False:
                lineTrack[lsCheck(chop,subHeads)]['names'][-1] = chop
                
        if lineTrack['currLineAttrib'][-1] == False:
            lineTrack['currLineAttrib'][-1] = checkSyntax(chop)
        if lineTrack['currLineAttrib'][-1] == False:
            lineTrack['currLineAttrib'][-1] = checkNames(chop)
        if lineTrack['currLineAttrib'][-1] == False:
            lineTrack['currLineAttrib'][-1] = checkDeclared(chop)
    elif n == '{':
        n = n+'\n'+add
    elif n == '}':
        n = add+n+'\n'
    elif n == ';':
        n = ';\n'+add
    
    if newLine == None:
       changeGlob('currLineChop',n)
    else:
        lineTrack['currLineChop'] = lineTrack['currLineChop'] + n
def getAtts(x,lsN):
    if ' is ' in x:
        atts = x.split(' is ')[1].split('{')[0].replace(' ,',',').split(',')
        for i in range(0,len(atts)):
            att = eatAll(atts[i],[' ','','\t','\n'])
            if att not in lsN:
                lsN.append(att)
    return lsN
def getHeadsName(x,y):
    na = x.split(y+' ')[1].split(' ')[0]
    if y not in lineTrack:
        lineTrack[y] = {'names':[]}
    if na not in lineTrack[y]['names']:
        lineTrack[y]['names'].append(na)
    if na not in lineTrack[y]:
        lineTrack[y][na] = {'attributes':[],'names':{},'funcs':[]}
    lineTrack[y][na]['attributes'] = getAtts(x,lineTrack[y][na]['attributes'])
    return na
def getTagName(x,y):
    na = eatAll(x.split(y)[1],[' ',';','','\n','\t'])
    if y not in lineTrack:
        lineTrack[y] = {'names':[]}
    lineTrack[y]['names'].append(na)
    return na
def getCurrJs():
    return lineTrack[getCurrSect()][getCurrName()]
def getCurrName():
    return lineTrack[getCurrSect()]['names'][-1]
def currNameCheck():
    if 'currSect' in lineTrack:
        if 'names' in lineTrack[getCurrSect()]:
            if len(lineTrack[getCurrSect()]['names'])>0:
                return True
    return False
def getCurrAtts():
    return lineTrack[getCurrSect()][getCurrName()]['attributes']
def inputCurrAtt(x):
    if x not in getCurrAtts():
        lineTrack[getCurrSect()][getCurrName()]['attributes'].append(x)
    else:
        input(x+' is already used as a attribute name for '+getCurrName())
def getCurrFuncs():
    return lineTrack[getCurrSect()][getCurrName()]['funcs']
def inputCurrFuncs(x):
    if x not in getCurrFuncs():
        lineTrack[getCurrSect()][getCurrName()]['funcs'].append(x)
    else:
        input(x+' is already used as a function name for '+getCurrName())
def getUsedLibrary(x):
    inputCurrAtt(x.split('using ')[1].split(' ')[0])
def getModName(x):
    na = x.split('modifier ')[1].split(' ')[0]
    if 'modifier' not in lineTrack[getCurrSect()][getCurrName()]:
        lineTrack[getCurrSect()][getCurrName()]['modifier'] = {'names':[],'funcs':[]}
    if na not in lineTrack[getCurrSect()][getCurrName()]['modifier']['names']:
        lineTrack[getCurrSect()][getCurrName()]['modifier']['names'].append(na)
        enclosed = getEnclosed(lines[defs['currLineI']:],['{','}'])
        if enclosed not in lineTrack[getCurrSect()][getCurrName()]['modifier']['funcs']:
            lineTrack[getCurrSect()][getCurrName()]['modifier']['funcs'].append(enclosed)
        else:
            input(enclosed+' is already designated as '+lineTrack[getCurrSect()][newNa]['modifier']['names'][findIt(na,+lineTrack[getCurrSect()][newNa]['modifier']['funcs'])])
    else:
        input(na+' is already used as: '+lineTrack[getCurrSect()][newNa]['modifier']['funcs'][findIt(na,lineTrack['modifier']['names'])])
def getFuncName(x):
    inputCurrFuncs(x.split('function ')[1].split('(')[0])
def getConstVals(x,lsN):
    constVars = x.split('constructor(')[1].split(')')[0].split(',')
    if constVars != '':
        for i in range(0,len(constVars)):
            js = {}
            breakDown = constVars[i].split(' ')
            for j in range(0,len(breakDown)):
                if j == 0:
                    for c in range(0,len(syntax["type"])):
                        ty = syntax["type"][c]
                        if breakDown[j][:len(ty)] == ty:
                            js['type'] = breakDown[j]
                elif j == (len(breakDown)-1):
                    js['name'] = breakDown[j]
                    print(js)
                elif j != 0 and j !=  (len(breakDown)-1):
                    for c in range(0,len(syntax["names"])):
                        tyNa = syntax["names"][c]
                        ty = syntax[tyNa]
                        for k in range(0,len(ty)):
                            if breakDown[j][:len(ty[k])] == ty[k]:
                                js[tyNa] = breakDown[j]
            lsN.append(js)
            
    return  lsN
def cleanLsMod(x,ls):
    lsN = []
    if type(x) is not list:
        x = [x]
    for i in range(0,len(x)):
        lsN.append(eatAll(x[i],ls).replace('\t',''))
    return lsN
def getCurrSect():
    return lineTrack['currSect']
def inputCurrSect(x):
    lineTrack['currSect'] = x
def getCurrSub():
    return lineTrack['currSub']
def inputCurrSub(x):
    lineTrack['currSub'] = x
def getSyntax(x):
    for i in range(0,len(syntax['names'])):
        na = syntax['names'][i]
        naLs = syntax[na]
        for j in range(0,len(naLs)):
            currNa = naLs[j]
            #print(x,currNa)
            if x[:len(currNa)] == currNa:
                return na
    return False
def cleanLs(lsOg):
    lsN = []
    ls = ['',' ']
    for i in range(0,len(lsOg)):
        if lsOg[i] not in ls:
            lsN.append(lsOg[i])
    return lsN
def headCheck(x):
    heads = defs['heads']
    for i in range(0,len(heads)):
        head = heads[i]
        if x in lineTrack[head]['names']:
            #print(x,head)
            return head
    return False
def namesCheck(x):
    heads = defs['heads']
    for i in range(0,len(heads)):
        head = heads[i]
        na = lineTrack[head]['names']
        for j in range(0,len(na)):
            if x in lineTrack[head][na[j]]['names']:
                return head,na[j]
    return False
def declaredCheck(x):
    for i in range(0,len(defs['variables'])):
        if 'name' in defs['variables'][i]:
            if x == defs['variables'][i]['name']:
                return defs['variables'][i]
    return False
def addressCheck(x):
    if '0x' in x:
        if len(x) == len('0x05BFC3F8E9124eCBc762f841eC540DB3987AFE82'):
            return True
    else:
        if len(x) == len('05BFC3F8E9124eCBc762f841eC540DB3987AFE82'):
            return True
    return False

def getVariableInfo(og):

    parts = cleanLs(og.split(' '))
    js = {}
    lsN = []

    for i in range(0,len(parts)):
        partSyn = getSyntax(parts[i])
        if partSyn != False:
            js[partSyn] = parts[i]
            lsN.append(partSyn)
        elif i == len(parts)-1:
            js['name'] = parts[i]
            lsN.append('name')
        elif headCheck(parts[i]) != False:
            head = headCheck(parts[i])
            if i == 0:
                na = parts[-1].split(';')[0]
                if parts[i] not in lineTrack[head][parts[i]]['names']:
                    lineTrack[head][parts[i]]['names'][na] = {'address':""}
                    
            else:
                na = js['name']
                if parts[i] not in lineTrack[head][parts[i]]['names']:
                    lineTrack[head][parts[i]]['names'][na] = {'address':""}
            lsN.append(head)
            js[head] = parts[i]
        elif namesCheck(parts[i]) != False:
            head,na = namesCheck(parts[i])
            if '=' in og:
                if na in og.split('=')[1]:
                    lineTrack[head][na]['names'][parts[i]]['address'] = og.split('=')[1].split(na+'(')[1].split(')')[0]
            lsN.append(head)
            js[head] = parts[i]
        elif addressCheck(parts[i]) != False:
            if 'variabes' not in lineTrack[getCurrSect()][getCurrName()]:
                lineTrack[getCurrSect()][getCurrName()]['variables'] = {parts[i]:{'address':add}}
                                 
        else:
            if 'False' not in js:
                js['False'] = []
            js['False'].append(parts[i])
            lsN.append(None)
    return js,lsN
def getForWhileInfo(x):
    na = eatAll(x.split('(')[0],[' ',';','','\n','\t'])
    lenNa = len(na+'(')
    nothing,z = getEnclosed(lines[defs['currLineI']:],['(',')'])
    if 'loops' not in lineTrack[getCurrSect()][getCurrName()]:
        lineTrack[getCurrSect()][getCurrName()]['loops'] = {'for':{'vars':[],'funcs':[]},'while':{'vars':[],'funcs':[]}}
    lineTrack[getCurrSect()][getCurrName()]['loops'][na]['vars'].append(cleanLsMod(nothing[0].split(na+'(')[1].split(')')[0].split(';'),[' ',';','','\n','\t']))
    lsN,z = getEnclosed(lines[defs['currLineI']:],['{','}'])
    lineTrack[getCurrSect()][getCurrName()]['loops'][na]['funcs'].append(cleanLsMod(lsN[1:-1],[' ',';','','\n','\t']))
    defs['currLineI'] = defs['currLineI']+len(lsN)
def getStructName(x):
    na = eatAll(x.split('struct')[1].split('{')[0],['',' ','\n','\t'])
    if 'structs' not in lineTrack[getCurrSect()][getCurrName()]:
        lineTrack[getCurrSect()][getCurrName()]['structs'] = {'names':[]}
    if na not in  lineTrack[getCurrSect()][getCurrName()]['structs']['names']:
        lineTrack[getCurrSect()][getCurrName()]['structs']['names'].append(na)
        lineTrack[getCurrSect()][getCurrName()]['structs'][na] = {'variables':[]}
    lsN,z = getEnclosed(lines[defs['currLineI']:],['{','}'])
    varis = z.split(';')[1:-1]
    for i in range(0,len(varis)):
        va = eatAll(varis[i],['',' ','\n','\t']).split(' ')
        if type(va) is not list:
            va = [va]
        lineTrack[getCurrSect()][getCurrName()]['structs'][na]['variables'].append({'type':eatAll(va[0],['',' ','\n','\t']).replace('\t',''),'name':eatAll(va[-1],['',' ','\n','\t'])})
    defs['currLineI'] = defs['currLineI'] + len(lsN)
def getMappingName(x):
    na = eatAll(x.split('mapping')[1].split(';')[0].split(' ')[1],['',' ','\n','\t'])
    if 'mapping' not in lineTrack[getCurrSect()][getCurrName()]:
        lineTrack[getCurrSect()][getCurrName()]['mapping'] = {'names':[],"funcs":[]}
    if na not in  lineTrack[getCurrSect()][getCurrName()]['mapping']['names']:
        lineTrack[getCurrSect()][getCurrName()]['mapping']['names'].append(na)
        lineTrack[getCurrSect()][getCurrName()]['mapping'][na] = {'variables':[]}
    lsN,z = getEnclosed(lines[defs['currLineI']:],['(',')'])
    varis = z.split(';')
    for i in range(0,len(varis)):
        va = varis[i].split(' ')
        if type(va) is not list:
            va = [va]
        lineTrack[getCurrSect()][getCurrName()]['mapping'][na]['variables'].append({'type':eatAll(va[0],['',' ','\n','\t']),'name':eatAll(va[-1],['',' ','\n','\t'])})
    defs['currLineI'] = defs['currLineI'] + len(lsN)
def isDeclare(x):
    for i in range(0,len(syntax['type'])):
        syn = syntax['type'][i]
        if x[:len(syn)] == syn:
            getVaraibleInfo(x)
def isCurr(x):
    ls = ['tags','heads','subHeads','loops']
    for i in range(0,len(ls)):
        currLs = ls[i]
        for j in range(0,len(defs[currLs])):
            curr = defs[currLs][j]
            if x[:len(curr)] == curr:
                if i == 0:
                    na = getTagName(x,curr)
                elif i == 1:
                    inputCurrSect(curr)
                    getHeadsName(x,curr)
                elif i == 2:
                    inputCurrSub(curr)
                    if j == 0:
                        if 'constructor' not in getCurrJs():
                            lineTrack[getCurrSect()][getCurrName()]['constructor'] = {'vars':[],'attributes':[]}
                        lineTrack[getCurrSect()][getCurrName()]['constructor']['vars'] = getConstVals(x,lineTrack[getCurrSect()][getCurrName()]['constructor']['vars'])  
                        lineTrack[getCurrSect()][getCurrName()]['constructor']['attributes'] = getAtts(x,lineTrack[getCurrSect()][getCurrName()]['constructor']['attributes'])
                    elif j == 1:
                        if 'modifier' not in getCurrJs():
                            lineTrack[getCurrSect()][getCurrName()]['modifier'] = {'names':[],'funcs':[]}
                        getModName(x)
                    elif j == 2:
                        getUsedLibrary(x)
                    elif j == 3:
                        getFuncName(x)
                    elif j == 4:
                        getStructName(x)
                    elif j == 5:
                        getMappingName(x)
                elif i == 3:
                    getForWhileInfo(x)
                return True
    return False
def lsCheck(x,ls):
    if x in ls:
        return x
    return False
def ifComm(x):
    if x[:len('//')] == '//':
        if 'SPDX-License-Identifier' not in x:
            return False
        return x+'\n'
    return x
global lineTrack,currLineChop       
lsChangeGlob(['lines','lsBrack'],[reader('NeFiFeeManager.sol').split('\n'),[0,0,'']])
lineTrack = {}

changeGlob("syntax",{ "names":["type","modifiers","visibility","precedence","globalVariables","precedence"],
                     "modifiers":["pure","view","payable","constant","immutable","anonymous","indexed","virtual","override"],
                     "precedence":["assert","block","coinbase","difficulty","number","block;number","timestamp","block;timestamp","msg","data","gas","sender","value","gas price","origin","revert","require","keccak256","ripemd160","sha256","ecrecover","addmod","mulmod","cryptography","this","super","selfdestruct","balance","codehash","send"],
                     "visibility":["public","private","external","internal"],
                     "modifiers":["pure","view","payable","constant","anonymous","indexed"],
                     "globalVariables":['abi.decode(bytes memory encodedData, (...)) returns (...)', 'abi.encode(...) returns (bytes memory)', 'abi.encodePacked(...) returns (bytes memory)',  'abi.encodeWithSelector(bytes4 selector, ...) returns (bytes memory)', 'abi.encodeCall(function functionPointer, (...)) returns (bytes memory)','abi.encodeWithSelector(functionPointer.selector, (...))', 'abi.encodeWithSignature(string memory signature, ...) returns (bytes memory)', 'to abi.encodeWithSelector(bytes4(keccak256(bytes(signature)), ...)', 'bytes.concat(...) returns (bytes memory)', 'arguments to one byte array<bytes-concat>`', 'string.concat(...) returns (string memory)', 'arguments to one string array<string-concat>`', 'block.basefee (uint)', 'block.chainid (uint)', 'block.coinbase (address payable)', 'block.difficulty (uint)', 'block.gaslimit (uint)', 'block.number (uint)', 'block.timestamp (uint)', 'gasleft() returns (uint256)', 'msg.data (bytes)', 'msg.sender (address)', 'msg.sig (bytes4)', 'msg.value (uint)', 'tx.gasprice (uint)', 'tx.origin (address)', 'assert(bool condition)', 'require(bool condition)', 'for malformed input or error in external component)', 'require(bool condition, string memory message)', 'condition is false (use for malformed input or error in external component). Also provide error message.', 'revert()', 'revert(string memory message)', 'blockhash(uint blockNumber) returns (bytes32)', 'keccak256(bytes memory) returns (bytes32)', 'sha256(bytes memory) returns (bytes32)', 'ripemd160(bytes memory) returns (bytes20)', 'ecrecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) returns (address)', 'the public key from elliptic curve signature, return zero on error', 'addmod(uint x, uint y, uint k) returns (uint)', 'arbitrary precision and does not wrap around at 2**256. Assert that k != 0 starting from version 0.5.0.', 'mulmod(uint x, uint y, uint k) returns (uint)', 'with arbitrary precision and does not wrap around at 2**256. Assert that k != 0 starting from version 0.5.0.', "this (current contract's type)", 'super', 'selfdestruct(address payable recipient)', '<address>.balance (uint256)', '<address>.code (bytes memory)', '<address>.codehash (bytes32)', '<address payable>.send(uint256 amount) returns (bool)', 'returns false on failure', '<address payable>.transfer(uint256 amount)', 'type(C).name (string)', 'type(C).creationCode (bytes memory)', 'type(C).runtimeCode (bytes memory)', 'type(I).interfaceId (bytes4)', 'type(T).min (T)', 'type(T).max (T)'],"sectionHeader":['contract','library','interface','abstract contract'],"allVars":['contract','library','pragma solidity','import','interface','abstract contract','constructor','function','modify','SPDX-License-Identifier'],
                     "type":["address","uint","string","bytes",'bool']})
changeGlob('defs',{})
defs['tags'] = ['//:','pragma solidity']
defs['heads']=['contract','abstract contract','interface','library']
defs['subHeads']=['constructor','modifier','using','function','struct','mapping']
defs['loops'] = ['for(','while(']
defs['currLineI'] = 0
defs['variables'] = []
changeGlob('subHead',[])
changeGlob('currHead',[])
changeGlob('currLicense',[])
changeGlob('currPragma',[])
changeGlob('currLineLs',[])
changeGlob('currLine',None)
changeGlob('newLine',None)
changeGlob('lineTrack',{'declared':[],'variables':[],'currLineChop':"",'currLineAttrib':[],'currPrase':"",'newLine':""})
all = []
currLine = ''
currPhrase = ''
for i in range(0,len(lines)):
    while ifComm(lines[i]) == False:
        i += 1
    line = ifComm(lines[i])
    defs['currLineI'] = i
    changeGlob('currLine',eatAll(line,[' ','\n','\t','']))
    changeGlob('currLineLs',[])
    lineTrack['currPhrase'] = ''
    lineTrack['newLine'] = ''
    if isCurr(currLine) == False and currLine != None:
        if currNameCheck() == True:
            if getCurrName() == 'NeFiFeeManager' and currLine not in ['[',']','{','}']:
                if getVariableInfo(currLine) != False:
                    js,jsN = getVariableInfo(currLine)
                    defs['variables'].append(js)
    print(i)  
    i = defs['currLineI']
print('sdffdsfsd')
pen(lineTrack,'lineTrack.txt')
pen(str(defs['variables']).replace('},','},\n'),'all.txt')
