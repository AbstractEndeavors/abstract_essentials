import sys
import os
import json
import webbrowser
def changeGlob(x,y):
    globals()[x] = y
    return y
def homeIt():
    curr = os.getcwd()
    slash = '//'
    if '//' not in str(curr):
        slash = '/'
    changeGlob('slash',slash)
    changeGlob('home',curr)
    return home,slash
homeIt()
sys.path.insert(0, os.getcwd().replace(os.getcwd().split(slash)[-1],''))
import PySimpleGUI as sg
import functions as fun
import guiFunctions as guiFun
def mkLs(lsJs,allKeys):
  jsN = {}
  for k in range(0,len(lsJs)):
    js = lsJs[k]
    for i in range(0,len(allKeys)):
      jsN = fun.mkJsLs(jsN,allKeys[i],js)
  return jsN
def getCombo(js,key):
  return sg.Text(str(key)+':'),guiFun.dropDown({"ls":js[key],"key":str(key),"default_value":js[key][0],"title":str(key),"disabled":False,"pad":(0,0),"change_submits":True,"enable_events":True})
def getAllCombo(js):
  keys,lsN = fun.getKeys(js),[]
  for k in range(0,len(keys)):
    lsN.append(getCombo(js,keys[k]))
  return lsN
def getJsLsSpec(jsLs,key,x):
  lsN = []
  for k in range(0,len(jsLs)):
    if jsLs[k][key] == x:
      lsN.append(jsLs[k])
  return lsN
def ensureAllKeysInJs(jsLs,keys):
  for k in range(0,len(jsLs)):
    for i in range(0,len(keys)):
      if keys[i] not in jsLs[k]:
        jsLs[k][keys[i]] = "None"
  return jsLs
def remIntVal(values):
  keys,jsN = fun.getKeys(values),{}
  for k in range(0,len(keys)):
    if str(keys[k]) != str(0):
      jsN[keys[k]] = values[keys[k]]
  return jsN
def getInitJsVals():
    jsLs = ensureAllKeysInJs(jsLsOg,allKeys)
    jsN = mkLs(jsLs,allKeys)
    return jsLs,jsN
def getJsVals(jsLs,event,values):
  jsLs = getJsLsSpec(jsLs,event,values[event])
  jsN = mkLs(jsLs,allKeys)
  return jsLs,jsN
def winWhile(window,typ):
  while True:
      event, values = window.read()
      values = remIntVal(values)
      if event == 'Auto':
          return 'Auto'
      if typ == 'add':
        ret = addRPCevents(values,event,window)
      elif typ == 'choose':
        ret = chooseRPCevents(values,event,window)
        fun.pen(json.dumps(values),'currRPCvals.json')

      if ret == 'EXIT':
        window.close()
        break
        return values
def runWinVals(window,jsN,event,values):
  window[event].update(value=values[event])
  for k in range(0,len(allKeys)):
      if allKeys[k] != 'netName':
        window[allKeys[k]].update(values=jsN[allKeys[k]])
        if len(jsN[allKeys[k]]) == 1:
          window[allKeys[k]].update(value=jsN[allKeys[k]])      
def createLayout(title,layout,typ):
    sg.set_options(suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False)
    menu_def = [['File',  'Save', 'Exit',],['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],['Help', 'About...'],]
    layout = [[sg.Menu(menu_def)],layout,[sg.OK('OK'),sg.Button('Show'),sg.Button('reset'),sg.Button('Exit')]]
    return winWhile(sg.Window(title, layout, finalize=True),typ)
def chooseRPCevents(values,event,window):
  global cou,jsLs
  if cou == 0:
    jsLs,jsN= getInitJsVals()
    cou +=1
  if event in allKeys:
    if event == 'netName':
      jsLs,jsN= getInitJsVals()
    jsLs,jsN=getJsVals(jsLs,event,values)
    runWinVals(window,jsN,event,values)    
  elif event == 'reset':
      jsLs,jsN = getInitJsVals()
  elif event == 'OK':
    fun.pen('rpcVal = '+json.dumps(values),'rpcValues.py')
    window.close()
    return 'EXIT'
  elif event == sg.WIN_CLOSED or event == 'Exit':
    window.close()
    return 'EXIT'
def addRPCevents(values,event,window):
  #if event == sg.WIN_CLOSED or event == 'Exit':
  #  webbrowser.get(chrome.open(value['BlockExplorer']))
  #  webbrowser.get(chrome.open(value['RPC']))
  #  return 'EXIT'
  if event == 'OK':
      rpcLs = fun.jsRead('RPCList.json')
      if value['NetworkName'] not in rpcLs['names']:
          rpcLs['names'].append(value['NetworkName'])
          rpcLs[value['NetworkName']]= []
      rpcLs[value['NetworkName']].append({'netName':value['NetworkName'],'chainId':value['chainId'],'RPC':value['RPC'],'nativeCurrency':value['nativeCurrency'],'blockExplorer':value['blockExplorer']})
      fun.pen(rpcLs,'RPCList.json')
      return 'EXIT'
def chooseDefaultRPC():
    jsLs,jsN = getInitJsVals()
    changeGlob('jsLs',jsLs)
    return createLayout('chooseRPC',getAllCombo(jsN),'choose')
def AddRPC():
    layout = [[sg.Text('Network Name'),sg.Input('',key='NetworkName'),sg.Push()],
              [sg.Text('network'),sg.Combo(['Mainnet','TestNet'],key='network'),sg.Push()],
              [sg.Text('nativeCurrency'),sg.Input('',key='nativeCurrency'),sg.Push()],
              [sg.Text('chainId'),sg.Input('',key='chainId'),sg.Push()],
              [sg.Text('RPC'),sg.Input('',key='RPC'),sg.Push()],[sg.Text('BlockExplorer'),sg.Input('',key='BlockExplorer'),sg.Push()],
              [sg.Text('RPC'),sg.Input('',key='contractName'),sg.Push()]]
    createLayout('addRPC',layout,'add')
global allKeys,jsLsOg,cou
cou = 0
allKeys,jsLsOg =  ['netName','nativeCurrency', 'network', 'RPC', 'chainId', 'blockExplorer'],fun.getrpcListNew()

