from web3 import Web3
import sys
import os
import json
import PySimpleGUI as sg
import codecs
import requests
from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
def avgGasPriceEstd():
    pending_transactions = web3.provider.make_request("parity_pendingTransactions", [])
    gas_prices,gases = [],[]
    for tx in pending_transactions["result"[:10]]:
        gas_prices.append(int((tx["gasPrice"]),16))
        gases.append(int((tx["gas"])))
    return statistics.median(gas_prices)
def avgGasPriceEst():
    req = requests.get('https://ethgasstation.info/json/ethgasAPI.json')
    t = json.loads(req.content)
    gas_price1 = web3.eth.gasPrice
    return int(t[gasSpeed]*(10**8))
def specificverifyInput(inType,inVar,outType,outVar,fun,ask):
    asky = ''
    layout = [[sg.Text(ask), sg.Yes()],
            [sg.Text('choose anther '+str(outVar)+' input:'), sg.No()],
            [sg.Yes(), sg.No()]]
    window = sg.Window('Window Title', layout)
    while asky == '':             
        event, values = window.read()
        print(values)
        if event in (sg.WIN_CLOSED, 'Cancel'):
            asky = False
        window.close()
        asky = True
    window.close()  
    return asky
def specificAskInput(inType,inVar,fun,ask):
    asky = ''
    y = asky
    layout = [
        [sg.Text(inType + ' '+ inVar), sg.Push(), sg.Input('', key=inType)],
        [sg.Text('Input Verification'), sg.Push(), sg.Input('', disabled=True, key='verify')],
        [sg.OK('OK'),sg.Button('Show'), sg.Button('Exit'),]]
    window = sg.Window(fun, layout)
    while asky == '':
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            asky = 'exit'
        if event == sg.OK() or event == 'OK':
            asky = values[inType]
        elif event == 'Show':
            x_string = values[inType]
            if 'address' in inType:
                y = addressVerify(inType,x_string)
                if y == False:
                    y = 'checkSum was unable to verify '+x_string+' '+inType
                else:
                    y = inType+' is good to go!'
            if 'uint' in inType:
                y = uintVerify(inVar,x_string)
                if y == False:
                    y = x_string+'is not a valid '+inType+' input'
                else:
                    y = inType+' is good to go!'
            window['verify'].update(value=y)
    window.close()
    return asky
def askList(nets):
    y = []
    sg.set_options(suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False)
    layout = [[sg.Text('functions:'),sg.Combo(nets, key='functions',default_value=nets[0]), sg.Push()],
    [sg.OK('OK'),sg.Button('Show'),sg.Button('Exit')]]
    window = sg.Window('Window Title', layout, finalize=True)
    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.OK() or event == 'OK':
            return values['functions']
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()
def specificTextInput(inType,inVar,qu,outType,outVar,fun,ask):
    layout = [
        [sg.Text(inType + ' '+ inVar), sg.Push(), sg.Input('', key='x')],
        [sg.Text(outType+' '+outVar), sg.Push(), sg.Input('', disabled=True, key='x+2')],
        [sg.Button('Show'), sg.Button('Exit')]]
    window = sg.Window(fun, layout)
    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Show':
            x_string = values['x']
            try:
               y = ans = grab.tryCheckSum(x_string)

            except ValueError:
                y = "Wrong number !!!"
            window['x+2'].update(value=y)
    window.close()
def simpleBool(ask):
    asky = ''
    layout = [[sg.Text(ask)],
            [sg.Yes(), sg.No()]]
    window = sg.Window('Window Title', layout)
    while asky == '':             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            asky = False
        window.close()
        asky = True
    window.close()  
    return asky
def mkBool(x):
    if str(x).lower() in ['true','t','yes','y','0']:
        return str(0)
    return str(1)    
def getType(ty,x):
    if 'int' in ty:
        return int(x)
    elif 'bytes' in ty:
        return kek(x)
    elif 'address' in ty:
        return w3.toChecksumAddress(str(x))
    elif 'bool' in ty:
        return bool(str(x))
    else:
        return str(x)
def cleanLs(ls):
    lsN = []
    for k in range(0,len(ls)):
        if ls[k] != '':
            lsN.append(ls[k])
    return lsN    
def ifLs(ty,x):
    x = cleanLs(mkLs(x.split(',')))
    for k in range(0,len(x)):
        x[k] = getType(ty,x[k])
    return x
def addressVerify(va,y):
    return tryCheckSum(str(y))
def uintVerify(va,y):
    return f.isInt(y)
def checkSum(x):
        return w3.toChecksumAddress(x)
def tryCheckSum(x):
    try:
        y = checkSum(x)
        return y
    except:
        return False
def safeSplit(x,y,k):
    if y in x:
        z = x.split(y)
        if len(z) > k:
            return z
def isAddress(x):
    if x[:len('address')] == 'address':
        return True
def isBool(x):
    if x[:len('bool')] == 'bool':
        return True
def isString(x):
    if x[:len('string')] == 'string':
        return True
def isBytes(x):
    if x[:len('bytes')] == 'bytes':
        return True
def isLs(ls):
    if type(ls) is list:
        return True
    return False
def isList(x):
    if x[-1] == ']':
        if x[:-1].split('[')[-1] == '':
            return [x],'*',0
        lsN = []
        for i in range(0,int(x[:-1].split('[')[-1])):
            lsN.append(x)    
        return lsN,i,0
    return x,1,0
def isUintSt(x):
    if x[:len('uint')] == 'uint' and str(x).lower() in ['uint8','uint16','uint32','uint64','uint128','uint256']:
        return True
    return False
def isIntSt(x):
    if x[:len('int')] == 'int' and str(x).lower() in ['int8','int16','int32','int64','int128','int256']:
        return True
    return False
def isInt(x):
  if type(x) is int:
    return True
  return False
def lsNum():
    return str('1,2,3,4,5,6,7,8,9,0').split(',')
def isNum(x):
    if isInt(x):
        return True
    for k in range(0,len(str(x))):
        if str(x)[k] not in lsNum():
            return False
    return True
def indetLoop(ty,k):
    tot = input('indeterminate '+str(ty)+' list, how many inputs will you be appending to it? (will inquire again at this input interval, otherise, inquiry will repeat every loop)')
    deff = f.isInt(tot)
    if deff == False:
        tot = k + 1
    return tot,deff
def listLoop(k,tot):
    print(str(k)+' out of '+str(tot)+' inputs in this list')
def denyInp(ty,va,fun,ans,exp):
    print('your '+str(ty)+' input for '+str(va)+' in function '+str(fun)+'; '+str(ans)+' was denied for '+exp)
def verify(ty,va,fun,ans):
    return specificverifyInput(ty,va,ty,ans,fun,'your '+str(ty)+' input for '+str(va)+' in functin '+str(fun)+' is '+str(ans)+' that ok?')
def askInput(ty,va,fun):
    return specificAskInput(ty,va,fun,'please input '+str(ty)+' for variable '+str(va)+' in function'+str(fun)+':')
def askBool(ty,va,fun):
    return specificAskInput(ty,va,fun,'please input '+str(ty)+' for variable '+str(va)+' in function'+str(fun)+':')
def inputUint(ty,va,fun):
    while isUintSt(ty):
        ast = False
        print('input will be multiplied by 10^'+str(int(18))+' if * is added to the end of the input)')
        ans = askInput(ty,va,fun)
        if ans[-1] == '*':
            ast,ans = True,ans[:-1]
        if isNum(ans):
            if ast == True:
                ans = int(float(int(ans))*float(str('1e'+str(int(18)))))
            if verify(ty,va,fun,ans):
                ifVarisLsApp(str(ans))
                return
def inputInt(ty,va,fun):
    while isIntSt(ty):
        ast = False
        print('input will be multiplied by 10^'+str(int(8))+' if * is added to the end of the input)')
        ans = askInput(ty,va,fun)
        if ans[-1] == '*':
            ast,ans = True,ans[:-1]
        if isNum(ans):
            if ast == True:
                ans = int(float(int(ans))*float(str('1e'+str(int(8)))))
            if verify(ty,va,fun,ans):
                ifVarisLsApp(str(ans))
                return
def ifVarisLsApp(x):
    if type(varis['inputs']['inpCurr'][-1]) is list:
        varis['inputs']['inpCurr'][-1].append(x)
    else:
        varis['inputs']['inpCurr'][-1] = x
def inputAddress(ty,va,fun):
    while isAddress(ty):
        ans = tryCheckSum(str(askInput(ty,va,fun)))
        if ans != False:
            if verify(ty,va,fun,ans) == True:
                ifVarisLsApp(ans)
                return 
        else:
            denyInp(ty,va,fun,ans,' bad checksum address')
def inputBool(ty,va,fun):
    while isBool(ty):
        ans = askBool(ty,va,fun)
        if verify(ty,va,fun,ans):
            if ans == True:
                ifVarisLsApp(ans)
            else:
                ifVarisLsApp(ans)
            return
def inputString(ty,va,fun):
    while isString(ty):
        ans = str(askInput(ty,va,fun))
        if verify(ty,va,fun,ans) == True:
            ifVarisLsApp(ans)
            return
def inputBytes(ty,va,fun):
    while isBytes(ty):
        ans = str(askInput(ty,va,fun))
        if verify(ty,va,fun,ans) == True:
            ifVarisLsApp(ans)
            return
def askAll(ty,va,fun):
    varis['inputs']['typeCurr'].append([ty,va,fun])
    varis['inputs']['inpCurr'].append(ty)
    deff = True
    tyAc,tot,cou = isList(ty)
    if type(ty) is list:
        if tot == '*':
            tot,deff = indetLoop(ty,cou)
        else:
            print('input requres list of a length '+str(tot)+'; the input request will repeat '+str(tot)+' times')
    while cou < tot:
        inputAddress(ty,va,fun)
        inputBool(ty,va,fun)
        inputString(ty,va,fun)
        inputBytes(ty,va,fun)
        inputUint(ty,va,fun)
        inputInt(ty,va,fun)
        cou += 1
        listLoop(cou,tot)
        if deff == False:
            tot = indetLoop(ty,cou)
def ifInput(js):
    lsType = ['address','uint','bool','bytes','string']
    if 'inputs' in js:

        inps = js['inputs']
        for i in range(0,len(inps)):
            if ' ' in inps[i]:
                askAll(inps[i].split(' ')[0],inps[i].split(' ')[-1],js['name'])
            else:
                 askAll(inps[i],inps[i],js['name'])
def homeIt():
	changeGlob("home",os.getcwd())
	slash = "//"
	if "//" not in str(home):
		slash = "/"
		changeGlob("slash",slash)
	return home,slash
def pen(paper, place):
	with open(place, "w") as f:
		f.write(str(paper))
		f.close()
		return
def isHex(x):
	try:
		z = x.hex()
		return True
	except:
		return False
def printHex(x):
	if isHex(x):
		return x.hex()
	return text
def changeGlob(x,v):
	globals()[x] = v
def readerC(file):
	with open(file,"r" ,encoding="utf-8-sig") as f:
		text = f.read()
		return text
def mkLs(ls):
  if type(ls) is not list:
    ls = [ls]
  return ls
def getCodex(x):
    b = get_hex_data(x)
    return codecs.decode(b, 'UTF-8')
def kek(x):
    st = '"'+str(x)+'"'
    return w3.keccak(text=str(x)).hex()
def read_hex(hb):
    h = "".join(["{:02X}".format(b) for b in hb])
    return h
def get_hex_data(x):
    n = len(x)
    hex = x
    return int(hex, n)
